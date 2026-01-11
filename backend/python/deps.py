from service.user_service import UserService
from service.token_service import TokenService
from service.protected_resource_service import ProtectedResourceService
from typing import Optional
from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from logger import Logger

log = Logger.get_logger(__name__)
user_service: Optional[UserService] = None
token_service: Optional[TokenService] = None
protected_resource_service: Optional[ProtectedResourceService] = None
bearer_scheme = HTTPBearer()

def get_user_service():
    global user_service
    if user_service is None:
        user_service = UserService()
    return user_service


def get_token_service():
    global token_service
    if token_service is None:
        token_service = TokenService()
    return token_service


def get_protected_resource_service():
    global protected_resource_service
    if protected_resource_service is None:
        protected_resource_service = ProtectedResourceService()
    return protected_resource_service

async def validate_protected_resource_api_request(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
                                                  user_service: UserService = Depends(get_user_service),
                                                  token_service: TokenService = Depends(get_token_service)):
    log.info(f"Validating protected resource api request...")
    decoded, err = token_service.validate_token(token=credentials.credentials)
    if err:
        raise HTTPException(status_code=401, detail=str(err))
    username = decoded.get('username', None)
    if username is None:
        raise HTTPException(status_code=403, detail="Token Claims Do Not Contain username")
    exists, err = await user_service.is_user_with_username_present(username)
    if err:
        raise HTTPException(status_code=401, detail=str(err))
    if not exists:
        raise HTTPException(status_code=401, detail="username in claims is not a valid user")
    return
