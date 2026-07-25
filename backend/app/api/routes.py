from uuid import UUID
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.auth import require_user, CurrentUser
from app.schemas.metadata import MetadataCreate, MetadataRead, SubmissionCreate, SubmissionRead
from app.services.metadata_service import MetadataService
router=APIRouter(dependencies=[Depends(require_user)])
def service(db:AsyncSession=Depends(get_db)): return MetadataService(db)
@router.get("/health")
async def health(): return {"status":"ok"}
@router.get("/metadata",response_model=list[MetadataRead])
async def list_metadata(s:MetadataService=Depends(service)): return await s.list()
@router.post("/metadata",response_model=MetadataRead,status_code=201)
async def create_metadata(body:MetadataCreate,s:MetadataService=Depends(service)): return await s.create(body)
@router.get("/metadata/{id}",response_model=MetadataRead)
async def get_metadata(id:UUID,s:MetadataService=Depends(service)): return await s.get(id)
@router.put("/metadata/{id}",response_model=MetadataRead)
async def update_metadata(id:UUID,body:MetadataCreate,s:MetadataService=Depends(service)): return await s.update(id,body)
@router.delete("/metadata/{id}",status_code=204)
async def delete_metadata(id:UUID,s:MetadataService=Depends(service)): await s.delete(id); return Response(status_code=204)
@router.get("/metadata/{id}/fields/{field_name}/options")
async def field_options(id:UUID,field_name:str,s:MetadataService=Depends(service)): return await s.options(id,field_name)
@router.post("/metadata/{id}/submissions",response_model=SubmissionRead,status_code=201)
async def submit(id:UUID,body:SubmissionCreate,user:CurrentUser=Depends(require_user),s:MetadataService=Depends(service)): return await s.submit(id,body,user)
