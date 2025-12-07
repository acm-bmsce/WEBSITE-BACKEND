from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List
from app.models.user import User, UserCreate
from app.auth import get_password_hash, verify_password, create_access_token, SECRET_KEY, ALGORITHM
from jose import JWTError, jwt

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# --- DEPENDENCIES (Security Checks) ---

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = await User.find_one(User.username == username)
    if user is None:
        raise credentials_exception
    return user

async def get_master_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "master":
        raise HTTPException(status_code=403, detail="Not authorized (Master Access Required)")
    return current_user

# --- ROUTES ---

# 1. REGISTER (Anyone can register, defaults to Pending Coordinator)
@router.post("/register", response_model=dict)
async def register(user_data: UserCreate):
    # Check if username exists
    existing_user = await User.find_one(User.username == user_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    # Create new user
    hashed_pw = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pw,
        role="coordinator",
        is_approved=False  # MUST be approved by Master later
    )
    await new_user.insert()
    return {"message": "Registration successful. Waiting for Master Admin approval."}

# 2. LOGIN (Generates Token)
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.find_one(User.username == form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    if not user.is_approved:
        raise HTTPException(status_code=403, detail="Account not approved yet by Master Admin")

    # Generate Token
    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

# 3. GET PENDING USERS (Master Only)
@router.get("/pending", dependencies=[Depends(get_master_admin)])
async def get_pending_users():
    users = await User.find(User.is_approved == False).to_list()
    return users

# 4. APPROVE USER (Master Only)
@router.patch("/{user_id}/approve", dependencies=[Depends(get_master_admin)])
async def approve_user(user_id: str):
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_approved = True
    await user.save()
    return {"message": f"User {user.username} approved!"}