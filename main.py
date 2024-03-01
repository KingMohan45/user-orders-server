import logging, sys

from dotenv import load_dotenv
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse

from app.users.routes import user_router
from app.orders.routes import orders_router
from config import settings

load_dotenv()

# logging
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(process)s %(levelname)s %(name)s %(module)s %(funcName)s %(lineno)s",
        },
        "standard": {
            "class": "logging.Formatter",
            "format": "%(asctime)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "json",
            "stream": sys.stderr,
        },
        "consolelog": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "stream": sys.stderr,
        },
    },
    "loggers": {
        "router": {"level": "DEBUG", "handlers": ["console"], "propagate": True},
        "root": {"level": "DEBUG", "handlers": ["consolelog"], "propagate": True},
        "celery": {"level": "DEBUG", "handlers": ["consolelog"], "propagate": True},
    },
}

logging.config.dictConfig(logging_config)

# API Docs
swagger_docs = "docs"
redoc_docs = "redoc"
if settings.ENVIRONMENT.lower() == "production":
    swagger_docs = None
    redoc_docs = None

app = FastAPI(
    title="User Orders Platform APIs",
    description="This is the documentation for the Order APIs",
    version="0.0.1",  # read this version from a config file
    contact={
        "name": "Mohan Kumar",
        "url": "https://github.com/kingmohan45",
        "email": "ragamsettymohankumar@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    docs_url=f"/{swagger_docs}" if swagger_docs else None,
    redoc_url=f"/{redoc_docs}" if redoc_docs else None,
)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # allow cookies
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=[
        "accept",
        "accept-encoding",
        "authorization",
        "content-type",
        "dnt",
        "origin",
        "user-agent",
        "x-csrftoken",
        "x-requested-with",
        "x-forwarded-proto",
        "x-api-key",
        "x-api-request-id",
    ],
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
app.add_middleware(GZipMiddleware, minimum_size=1000)


# API Docs Routex
@app.get(
    "/",
    response_class=HTMLResponse,
    tags=["Welcome to User Orders Management Platform"],
    include_in_schema=False,
)
def documentation():
    # ToDo: read the context from an html file.
    context = f"""
    <html>
        <head>
            <title>User Orders Management Platform</title>
        </head>
        <body>
            <h1>Welcome to the User Orders Management Platform API documentation</h1>
            <a href='{redoc_docs}'>Redoc style documentation</a><br>
            <a href='{swagger_docs}'>Swagger style documentation</a>
        </body>
    </html>
    """
    if settings.ENVIRONMENT.lower() == "production":
        return RedirectResponse(url=settings.UI_HOST, status_code=status.HTTP_302_FOUND)
    return HTMLResponse(content=context)


app.include_router(user_router)
app.include_router(orders_router)
