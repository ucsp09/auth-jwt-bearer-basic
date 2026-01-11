from enum import Enum

class TokenType(Enum):
    BEARER = 'Bearer'

class TokenSigningAlgorithm(Enum):
    HS256 = 'HS256'