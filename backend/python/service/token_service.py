from logger import Logger
import jwt
from jwt.api_jwk import PyJWK
from typing import Any
from enums import TokenSigningAlgorithm
from datetime import datetime, timezone, timedelta
from constants import JWT_EXPIRES_IN_SECONDS, JWT_ISSUER_NAME, JWT_AUDIENCE_NAME, JWT_TOKEN_SIGNING_SHARED_SECRET

log = Logger.get_logger(__name__)

class TokenService:
    def __init__(self):
        pass

    def _get_claims_for_user(self, username: str):
        try:
            payload = {
                "username": username,
                "sub": username,
                "iss": JWT_ISSUER_NAME,
                "aud": JWT_AUDIENCE_NAME,
                "iat": datetime.now(tz=timezone.utc),
                "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=JWT_EXPIRES_IN_SECONDS) 
            }
            return payload, None
        except Exception as e:
            return None, e

    def _get_token_with_hs256_algorithm(self, payload: dict, key: Any | PyJWK | str | bytes):
        try:
            token = jwt.encode(payload=payload,
                               key=key,
                               algorithm=TokenSigningAlgorithm.HS256.value)
            return token, None
        except Exception as e:
            return None, e
        
    def _get_token_with_algorithm(self, payload: dict, key: Any | PyJWK | str | bytes, algorithm: TokenSigningAlgorithm):
        try:
            if algorithm == TokenSigningAlgorithm.HS256:
                return self._get_token_with_hs256_algorithm(payload=payload, key=key)
            else:
                return None, f"Token Signing Algorithm:{TokenSigningAlgorithm.name} Not Supported"
        except Exception as e:
            return None, e

    def _verify_and_decode_token_with_hs256_algorithm(self, token: str, key: Any | PyJWK | str | bytes, issuer: str, audience: str):
        try:
            decoded = jwt.decode(jwt=token,
                                 key=key,
                                 algorithms=[TokenSigningAlgorithm.HS256.value],
                                 verify=True,
                                 issuer=issuer,
                                 audience=audience)
            return decoded, None
        except Exception as e:
            return None, e

    def _verify_and_decode_token_with_algorithm(self, token: str, key: Any | PyJWK | str | bytes, algorithm: TokenSigningAlgorithm, issuer: str, audience: str):
        try:
            if algorithm == TokenSigningAlgorithm.HS256:
                return self._verify_and_decode_token_with_hs256_algorithm(token, key, issuer, audience)
            else:
                return None, f"Token Signing Algorithm:{TokenSigningAlgorithm.name} Not Supported"
        except Exception as e:
            return None, e

    def generate_token(self, username: str):
        try:
            log.info(f"Generating token for user with username:{username}...")
            claims, err = self._get_claims_for_user(username)
            if err:
                return None, err
            return self._get_token_with_algorithm(
                payload=claims,
                key=JWT_TOKEN_SIGNING_SHARED_SECRET,
                algorithm=TokenSigningAlgorithm.HS256
            )
        except Exception as e:
            log.error(f"Error occured while generating token for user with username:{username}!!!Error:{e}")
            return None, e
        
    def validate_token(self, token: str):
        try:
            log.info("Validating token...")
            decoded, err = self._verify_and_decode_token_with_algorithm(
                token=token, key=JWT_TOKEN_SIGNING_SHARED_SECRET,
                algorithm=TokenSigningAlgorithm.HS256,
                issuer=JWT_ISSUER_NAME,
                audience=JWT_AUDIENCE_NAME
            )
            if err:
                return None, err
            return decoded, None
        except Exception as e:
            log.error(f"Error occured while validatin token!!!Error:{e}")
            return None, e
