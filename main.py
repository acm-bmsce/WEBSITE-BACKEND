from fastapi import FastAPI
from app.database import init_db
from app.routes import event_routes
from fastapi.middleware.cors import CORSMiddleware
from app.routes import project_routes
from app.routes import user_routes

app = FastAPI()

# Allow React to talk to FastAPI (CORS)
# We allow localhost:3000 (standard React) and 5173 (Vite)
origins = [
    "http://localhost:3000",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],
)

# Connect to Database when app starts
@app.on_event("startup")
async def start_db():
    await init_db()

# Register the routes
app.include_router(event_routes.router, prefix="/app/events", tags=["Events"])
app.include_router(project_routes.router, prefix="/app/projects", tags=["Projects"])
app.include_router(user_routes.router, prefix="/auth", tags=["Authentication"])

@app.get("/")
def read_root():
    return {"message": "Vitalyze Club Backend is Running!"}