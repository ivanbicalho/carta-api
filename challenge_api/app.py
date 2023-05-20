import logging
from fastapi import FastAPI
import challenge_route

app = FastAPI(
    title="Python Automation Course - Challenge",
    description="Challenge - Python Automation Course",
    terms_of_service="",
    contact={
        "Developer name": "Ivan Bicalho",
        "email": "ivan.bicalho@carta.com",
        "Website Address": "https://carta.com",
    },
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


app.include_router(challenge_route.router)
