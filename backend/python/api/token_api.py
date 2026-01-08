from fastapi.routing import APIRouter

token_api_router = APIRouter()

@token_api_router.post("/api/v1/token")
def get_token():
    pass
