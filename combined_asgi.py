# combined_asgi.py
import os
import django
from fastapi_app.main import app as api  # استيراد FastAPI app
from django.core.asgi import get_asgi_application
from starlette.middleware.wsgi import WSGIMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

# FastAPI with CORS if needed
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create main app that combines both
main_app = FastAPI()

# Include FastAPI under a custom path like "/api"
main_app.mount("/api", api)

# Mount Django under root "/"
main_app.mount("/", WSGIMiddleware(get_asgi_application()))
