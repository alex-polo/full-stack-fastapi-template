from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/login")
async def login() -> dict[str, str]:
    """Handle user login."""
    return {"message": "Login successful"}


@auth_router.post("/logout")
async def logout() -> dict[str, str]:
    """Handle user logout."""
    return {"message": "Logout successful"}


@auth_router.post("/register")
async def register() -> dict[str, str]:
    """Handle user registration."""
    return {"message": "Register successful"}


@auth_router.post("/refresh")
async def refresh() -> dict[str, str]:
    """Handle token refresh."""
    return {"message": "Refresh successful"}
