from constants import ADMIN_USERNAME, ADMIN_PASSWORD
from logger import Logger

log = Logger.get_logger(__name__)

class UserService:
    def __init__(self):
        pass

    async def is_user_with_username_present(self, username: str):
        try:
            log.info(f"Checking if user with username:{username} is present or not...")
            if username == ADMIN_USERNAME:
                log.info(f"User with username:{username} is present!!!")
                return True, None
            log.info(f"User with username:{username} is not present!!!")
            return False, None
        except Exception as e:
            log.error(f"Error occured while checking if user with username:{username} is present!!!Error:{e}")
            return None, e
    
    async def validate_password_for_user(self, username: str, password: str):
        try:
            log.info(f"Validating password for user with username:{username}...")
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                log.info(f"Password validation successfull for user with username:{username}!!!")
                return True, None
            log.info(f"Password validation failed for user with username:{username}!!!")
            return False, None
        except Exception as e:
            log.error(f"Error occured while validating password for user with username:{username}!!!Error:{e}")
            return None, e
