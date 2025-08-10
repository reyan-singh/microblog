from fastapi import FastAPI
from app.api.routers import auth, posts # Add other routers like posts, users
# app/main.py
# ...
from app.api.routers import auth, posts, users # <-- add users
from app.api.routers import auth, posts, users, timeline
# ...
from fastapi import FastAPI
from app.core.logging_config import setup_logging
setup_logging() # <-- Call the function

# app = FastAPI(...)
app = FastAPI(
    title="Scalable Microblogging Service",
    description="A take-home assignment to build a Twitter-like service."
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Microblogging Service!"}

# Include the routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(timeline.router, prefix="/timeline", tags=["Timeline"])