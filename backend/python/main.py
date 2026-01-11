from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from api.token_api import token_api_router
from api.protected_resource_api import protected_resource_api_router
from logger import Logger
from deps import validate_protected_resource_api_request

logger = Logger.get_logger(__name__)

logger.info("Initializing app...")
app = FastAPI()
logger.info("Adding middlewares...")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_headers="*",
    allow_methods="*")
logger.info("Adding routers...")
app.include_router(token_api_router)
app.include_router(protected_resource_api_router, 
                   dependencies=[Depends(validate_protected_resource_api_request)])
logger.info("App initialized successfully!!!")