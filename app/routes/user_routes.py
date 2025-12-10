from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from beanie import PydanticObjectId
from typing import List
from jose import JWTError, jwt

# Import Models
from app.models.user import User, UserCreate, AdminResetPassword

# ✅ Import Auth Helpers & Settings
from app.auth import get_password_hash, verify_password, create_access_token
from app.config import settings

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# --- DEPENDENCY: Get Current User ---
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # ✅ Decode using Secret from .env
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = await User.find_one(User.username == username)
    if user is None:
        raise credentials_exception
    return user

# --- DEPENDENCY: Check if Master Admin ---
async def get_master_admin(current_user: User = Depends(get_current_user)):
    # Simple check: assuming 'admin' is the master username
    # You can also check roles here e.g. if current_user.role != 'master'
    if current_user.username != "admin": 
        raise HTTPException(status_code=403, detail="Not authorized")
    return current_user

# ---------------------------------------------------------
# AUTH ROUTES
# ---------------------------------------------------------

@router.post("/register", response_model=User)
async def register(user_data: UserCreate):
    # Check if exists
    if await User.find_one(User.username == user_data.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    if await User.find_one(User.email == user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    hashed_pass = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username, 
        email=user_data.email, 
        hashed_password=hashed_pass,
        is_approved=False # Default to False
    )
    await new_user.insert()
    return new_user

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.find_one(User.username == form_data.username)
    
    # 1. Check User Exists & Password
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    # 2. Check Approval (Except for Master Admin)
    if user.username != "admin" and not user.is_approved:
        raise HTTPException(status_code=401, detail="Account pending approval by Master Admin.")

    # 3. Generate Token
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# ---------------------------------------------------------
# ADMIN MANAGEMENT ROUTES
# ---------------------------------------------------------

@router.get("/pending", dependencies=[Depends(get_master_admin)])
async def get_pending_users():
    return await User.find(User.is_approved == False).to_list()

@router.patch("/{user_id}/approve", dependencies=[Depends(get_master_admin)])
async def approve_user(user_id: PydanticObjectId):
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_approved = True
    await user.save()
    return {"message": f"User {user.username} approved."}

# ---------------------------------------------------------
# PASSWORD RESET FLOW
# ---------------------------------------------------------

@router.post("/request-reset")
async def request_password_reset(username: str):
    user = await User.find_one(User.username == username)
    if user:
        user.reset_requested = True
        await user.save()
    # Security: Always return same message
    return {"message": "Request sent to Master Admin."}

@router.get("/reset-requests", dependencies=[Depends(get_master_admin)])
async def get_reset_requests():
    return await User.find(User.reset_requested == True).to_list()

@router.post("/approve-reset", dependencies=[Depends(get_master_admin)])
async def approve_reset_password(data: AdminResetPassword):
    user = await User.get(PydanticObjectId(data.user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.hashed_password = get_password_hash(data.new_password)
    user.reset_requested = False
    await user.save()
    
    return {"message": "Password reset successfully."}