import asyncio
from app.database import init_db
from app.models.user import User
from app.auth import get_password_hash

async def create_master():
    await init_db()
    
    username = "BMSCEACM_MASTER"  # CHANGE THIS
    password = "BMSCEACM@2025" # CHANGE THIS
    
    # Check if exists
    exists = await User.find_one(User.username == username)
    if exists:
        print("Master Admin already exists.")
        return

    hashed = get_password_hash(password)
    master = User(
        username=username,
        email="acm@bmsce.ac.in",
        hashed_password=hashed,
        role="master",
        is_approved=True # Auto-approve the first master
    )
    await master.insert()
    print("Master Admin created successfully!")

if __name__ == "__main__":
    asyncio.run(create_master())