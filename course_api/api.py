import logging

from fastapi import FastAPI
from routes import message_route, number_route

app = FastAPI(
    title="Python Automation Course",
    description="Carta - Python Automation Course",
    terms_of_service="",
    contact={
        "Developer name": "Ivan Bicalho",
        "email": "ivan.bicalho@carta.com",
        "Website Address": "https://carta.com",
    },
    version="0.1.0",
    docs_url="/",
    redoc_url="/redoc",
)


app.include_router(message_route.router)
app.include_router(number_route.router)
