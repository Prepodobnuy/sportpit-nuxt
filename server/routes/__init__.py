from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from .admin_routes import router as admin_router
from .routes import router as default_router
from .auth import router as auth_router


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

router = APIRouter(prefix="/api")

router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(default_router, prefix="/client", tags=["Client"])
router.include_router(admin_router, prefix="/admin", tags=["Admin"])

app.include_router(router)


def run():
    import uvicorn

    uvicorn.run(app="routes:app", workers=20, reload=True)
    ...
