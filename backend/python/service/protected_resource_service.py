from logger import Logger
from aiofile import AIOFile
import json
from uuid import uuid4
import os

log = Logger.get_logger(__name__)

class ProtectedResourceService:
    def __init__(self):
        self.protected_resource_data_file_path = 'data/protected_resources.json'
    
    async def _get_protected_resources_from_db(self):
        try:
            log.debug(f"Getting protected resources from db...")
            if not os.path.exists(os.path.dirname(self.protected_resource_data_file_path)):
                os.makedirs(os.path.dirname(self.protected_resource_data_file_path), exist_ok=True)
            if not os.path.exists(self.protected_resource_data_file_path):
                return {}, None
            async with AIOFile(self.protected_resource_data_file_path, 'r') as afp:
                data = await afp.read()
                json_data = json.loads(data)
                return json_data, None
        except Exception as e:
            log.error(f"Error occured while getting protected resources from db!!!Error:{e}")
            return None, e  

    async def _save_protected_resources_to_db(self, data: dict):
        try:
            log.debug(f"Saving protected resources to db...")
            async with AIOFile(self.protected_resource_data_file_path, 'w') as afp:
                await afp.write(json.dumps(data, indent=4))
                return True, None
        except Exception as e:
            log.error(f"Error occured while saving protected resources to db!!!Error:{e}")
            return None, e

    async def is_protected_resource_with_resource_id_exists(self, resource_id: str):
        try:
            log.info(f"Getting all protected resources from db...")
            protected_resources, err = await self._get_protected_resources_from_db()
            if err:
                return None, err
            log.info(f"Checking if protected resource with resourceId:{resource_id} exists...")
            if resource_id in protected_resources:
                log.info(f"Protected Resource with resourceId:{resource_id} exists!!!")
                return True, None
            log.info(f"Protected Resource with resourceId:{resource_id} does not exist!!!")
            return False, None
        except Exception as e:
            log.error(f"Error occured while checking if protected resource with resourceId:{resource_id} exists!!!Error:{e}")
            return None, e
        
    async def is_protected_resource_with_resource_name_exists(self, resource_name: str):
        try:
            log.info(f"Getting all protected resources from db...")
            protected_resources, err = await self._get_protected_resources_from_db()
            if err:
                return None, err
            log.info(f"Checking if protected resource with name:{resource_name} exists...")
            for _, info in protected_resources.items():
                if info['name'] == resource_name:
                    log.info(f"Protected Resource with name:{resource_name} exists!!!")
                    return True, None
            log.info(f"Protected Resource with name:{resource_name} does not exist!!!")
            return False, None
        except Exception as e:
            log.error(f"Error occured while checking if protected resource with name:{resource_name} exists!!!Error:{e}")
            return None, e
        
    async def create_protected_resource(self, resource_info: dict):
        try:
            log.info(f"Getting all protected resources from db...")
            protected_resources, err = await self._get_protected_resources_from_db()
            if err:
                return None, err
            resource_id = uuid4().hex
            resource_info['resourceId'] = resource_id
            log.info(f"Creating protected resource with resourceId:{resource_id}...")
            protected_resources[resource_id] = resource_info
            success, err = await self._save_protected_resources_to_db(data=protected_resources)
            if err:
                return None, err
            if not success:
                return None, "Failed to save protected resource to db!!!"
            return resource_info, None
        except Exception as e:
            log.error(f"Error occured while creating protected resource!!!Error:{e}")
            return None, e

    async def get_all_protected_resources(self):
        try:
            log.info("Getting all protected resources from db...")
            protected_resources, err = await self._get_protected_resources_from_db()
            if err:
                return None, err
            return protected_resources, None
        except Exception as e:
            log.error(f"Error occured while getting all protected resources!!!Error:{e}")
            return None, e
        
    async def get_protected_resource(self, resource_id: str):
        try:
            log.info("Getting all protected resources from db...")
            protected_resources, err = await self._get_protected_resources_from_db()
            if err:
                return None, err
            log.info(f"Checking if protected resource with resourceId:{resource_id} exists or not...")
            if resource_id in protected_resources:
                log.info(f"Protected resource with resourceId:{resource_id} exists!!!")
                return protected_resources[resource_id], None
            log.info(f"Protected Resource with resourceId:{resource_id} does not exist!!!")
            return None, f"Protected Resource with resourceId:{resource_id} does not exist!!!"
        except Exception as e:
            log.error(f"Error occured while getting protected resource with resourceId:{resource_id}!!!Error:{e}")
            return None, e

    async def update_protected_resource(self, resource_id: str, data: dict):
        try:
            log.info("Getting all protected resources from db...")
            protected_resources, err = await self._get_protected_resources_from_db()
            if err:
                return None, err
            log.info(f"Updating protected resource with resourceId:{resource_id}...")
            resource_info = protected_resources[resource_id]
            for k, v in data.items():
                if v is not None:
                    resource_info[k] = v
            protected_resources[resource_id] = resource_id
            success, err = await self._save_protected_resources_to_db(data=protected_resources)
            if err:
                return None, err
            if not success:
                return None, "Failed to save protected resource to db!!!"
            log.info(f"Updated protected resource with resourceId:{resource_id} successfully!!!")
            return resource_info, None
        except Exception as e:
            log.error(f"Error occured while updating protected resource with resourceId:{resource_id}!!!Error:{e}")
            return None, e

    async def delete_protected_resource(self, resource_id: str):
        try:
            log.info("Getting all protected resources from db...")
            protected_resources, err = await self._get_protected_resources_from_db()
            if err:
                return None, err
            log.info(f"Deleting protected resource with resourceId:{resource_id}...")
            protected_resources.pop(resource_id, None)
            success, err = await self._save_protected_resources_to_db(data=protected_resources)
            if err:
                return None, err
            if not success:
                return None, "Failed to save protected resource to db!!!"
            log.info(f"Deleted protected resource with resourceId:{resource_id} successfully!!!")
            return True, None
        except Exception as e:
            log.error(f"Error occured while deleting protected resource with resourceId:{resource_id}!!!Error:{e}")
            return None, e
