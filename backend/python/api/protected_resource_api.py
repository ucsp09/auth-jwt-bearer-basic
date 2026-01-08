from fastapi.routing import APIRouter

protected_resource_api_router = APIRouter()

@protected_resource_api_router.post("/api/v1/protected/resources")
def create_protected_resource():
    pass

@protected_resource_api_router.get("/api/v1/protected/resources")
def get_all_protected_resources():
    pass

@protected_resource_api_router.get("/api/v1/protected/resources/{resourceId}")
def get_protected_resource():
    pass

@protected_resource_api_router.put("/api/v1/protected/resources/{resourceId}")
def update_protected_resource():
    pass

@protected_resource_api_router.delete("/api/v1/protected/resources/{resourceId}")
def delete_protected_resource():
    pass