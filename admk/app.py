from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware

from admk.router.generate import router as generate_router
from admk.router.detect import router as detect_router
from admk.router.test import router as test_router

app = FastAPI()
app.add_middleware(
    SessionMiddleware,
    secret_key="secret",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://10.108.25.241:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(generate_router)
app.include_router(detect_router)
app.include_router(test_router)