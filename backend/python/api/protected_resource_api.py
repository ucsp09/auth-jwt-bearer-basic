from fastapi.routing import APIRouter
from fastapi import HTTPException, Depends
from schema.protected_resource_schema import GetProtectedResourceAPIResponseSchema, GetAllProtectedResourceAPIResponseSchema, \
CreateProtectedResourceAPIRequestSchema, CreateProtectedResourceAPIResponseSchema, UpdateProtectedResourceAPIRequestSchema, \
UpdateProtectedResourceAPIResponseSchema, DeleteProtectedResourceAPIResponseSchema, GetTokenStatusAPIResponseSchema
from deps import get_protected_resource_service
from service.protected_resource_service import ProtectedResourceService

protected_resource_api_router = APIRouter()

@protected_resource_api_router.get("/api/v1/token/status")
async def get_token_status():
    return GetTokenStatusAPIResponseSchema(status="Token is valid")

@protected_resource_api_router.post("/api/v1/protected/resources")
async def create_protected_resource(input: CreateProtectedResourceAPIRequestSchema, protected_resource_service: ProtectedResourceService = Depends(get_protected_resource_service)):
    # Check if protected resource with same name already exists.
    exists, err = await protected_resource_service.is_protected_resource_with_resource_name_exists(resource_name=input.name)
    if err:
        raise HTTPException(status_code=500, detail=str(err))
    if exists:
        raise HTTPException(status_code=409, detail=f"Protected Resource With name:{input.name} already exists")
    
    # If resource with same name does not exist, then create the protected resource and return it
    protected_resource, err = await protected_resource_service.create_protected_resource(resource_info=input.model_dump())
    if err:
        raise HTTPException(status_code=500, detail=str(err))
    return CreateProtectedResourceAPIResponseSchema(
        resourceId=protected_resource['resourceId'],
        name=protected_resource['name'],
        description=protected_resource['description']
    )

@protected_resource_api_router.get("/api/v1/protected/resources")
async def get_all_protected_resources(protected_resource_service: ProtectedResourceService = Depends(get_protected_resource_service)):
    # Get all protected resources and return them
    protected_resources, err = await protected_resource_service.get_all_protected_resources()
    if err:
        raise HTTPException(status_code=500, detail=str(err))
    items = []
    for _, resource in protected_resources.items():
        items.append(GetProtectedResourceAPIResponseSchema(
            resourceId=resource['resourceId'], 
            name=resource['name'], 
            description=resource['description']))
    return GetAllProtectedResourceAPIResponseSchema(items=items, total=len(items))

@protected_resource_api_router.get("/api/v1/protected/resources/{resourceId}")
async def get_protected_resource(resource_id: str, protected_resource_service: ProtectedResourceService = Depends(get_protected_resource_service)):
    # Check if protected resource with resourceId exists.
    exists, err = await protected_resource_service.is_protected_resource_with_resource_id_exists(resource_id=resource_id)
    if err:
        raise HTTPException(status_code=500, detail=str(err))
    if not exists:
        raise HTTPException(status_code=404, detail=f"Protected Resource With resourceId:{resource_id} not found")
    
    # If protected resource with resourceId exists, return the protected resource
    protected_resource, err = await protected_resource_service.get_protected_resource(resource_id=resource_id)
    if err:
        raise HTTPException(status_code=500, detail=str(err))
    return GetProtectedResourceAPIResponseSchema(
        resourceId=protected_resource['resourceId'],
        name=protected_resource['name'],
        description=protected_resource['description']
    )

@protected_resource_api_router.put("/api/v1/protected/resources/{resourceId}")
async def update_protected_resource(resource_id: str,  input: UpdateProtectedResourceAPIRequestSchema, protected_resource_service: ProtectedResourceService = Depends(get_protected_resource_service)):
    # Check if protected resource with resourceId exists.
    exists, err = await protected_resource_service.is_protected_resource_with_resource_id_exists(resource_id=resource_id)
    if err:
        raise HTTPException(status_code=500, detail=str(err))
    if not exists:
        raise HTTPException(status_code=404, detail=f"Protected Resource With resourceId:{resource_id} not found")

    # If protected resource with resourceID exists, then update the protected resource and return it
    protected_resource, err = await protected_resource_service.update_protected_resource(resource_id=resource_id, data=input.model_dump())
    if err:
        raise HTTPException(status_code=500, detail=str(err))
    return UpdateProtectedResourceAPIResponseSchema(
        resourceId=protected_resource['resourceId'],
        name=protected_resource['name'],
        description=protected_resource['description']
    )

@protected_resource_api_router.delete("/api/v1/protected/resources/{resourceId}")
async def delete_protected_resource(resource_id: str, protected_resource_service: ProtectedResourceService = Depends(get_protected_resource_service)):
    # Check if protected resource with resourceID exists.
    exists, err = await protected_resource_service.is_protected_resource_with_resource_id_exists(resource_id=resource_id)
    if err:
        raise HTTPException(status_code=500, detail=str(err))
    if not exists:
        raise HTTPException(status_code=404, detail=f"Protected Resource With resourceId:{resource_id} not found")
    
    # If protected resource with resourceID exists, then deleted the protected resource
    success, err = await protected_resource_service.delete_protected_resource(resource_id=resource_id)
    if err:
        raise HTTPException(status_code=500, detail=str(err))
    if not success:
        raise HTTPException(status_code=500, detail=f"Failed to delete protected resource with resourceId={resource_id}")
    return DeleteProtectedResourceAPIResponseSchema(message=f"Deleted protected resource with resourceId:{resource_id} successfully!!!")    