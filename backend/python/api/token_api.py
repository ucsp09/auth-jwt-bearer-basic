from fastapi.routing import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from schema.token_schema import TokenRequestSchema, TokenResponseSchema
from service.user_service import UserService
from service.token_service import TokenService
from deps import get_user_service, get_token_service
from enums import TokenType
from constants import JWT_EXPIRES_IN_SECONDS

token_api_router = APIRouter()

@token_api_router.post("/api/v1/token")
async def get_token(input: TokenRequestSchema, 
              user_service: UserService = Depends(get_user_service), 
              token_service: TokenService = Depends(get_token_service)):
    # Check if user with username is present
    present, err = await user_service.is_user_with_username_present(input.username)
    if err:
        raise HTTPException(status_code=500, detail=str(err))
    if not present:
        raise HTTPException(status_code=401, detail="Invalid username!!!")

    # If user with username is present, validate the password
    success, err = await user_service.validate_password_for_user(input.username, input.password)
    if err:
        raise HTTPException(status_code=500, detail=str(err))
    if not success:
        raise HTTPException(status_code=401, detail="Invalid password!!!")
    
    # If password validation is successfull, generate token and return it
    token, err = token_service.generate_token(input.username)
    if err:
        raise HTTPException(status_code=500, detail=str(err))
    return TokenResponseSchema(access_token=token, 
                               token_type=TokenType.BEARER.value, 
                               expires_in=JWT_EXPIRES_IN_SECONDS)
