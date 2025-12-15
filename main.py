from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db

# Import Config
from app.config import settings # ✅ Import Settings

# Import Routes
from app.routes import event_routes
from app.routes import project_routes
from app.routes import user_routes
from app.routes import insight_routes

app = FastAPI()

# --- CORS CONFIGURATION ---
# We allow localhost for development + the URL defined in .env for production
origins = [     
    settings.FRONTEND_URL         
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def start_db():
    await init_db()

# Register Routes
app.include_router(event_routes.router, prefix="/events", tags=["Events"])
app.include_router(project_routes.router, prefix="/projects", tags=["Projects"])
app.include_router(user_routes.router, prefix="/auth", tags=["Authentication"])
app.include_router(insight_routes.router, prefix="/insights", tags=["Insights"])

@app.get("/")
def read_root():
    return {"message": "ACM Club Backend is Running!"}