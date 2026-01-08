from pydantic import BaseModel

class TokenRequestSchema(BaseModel):
    username: str
    password: str

class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str
    expires_in: int