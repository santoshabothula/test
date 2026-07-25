from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.models.entities import MetadataEntity, SubmissionEntity
from app.schemas.metadata import MetadataCreate, SubmissionCreate, DataType
class MetadataService:
    def __init__(self, db: AsyncSession): self.db=db
    def out(self,e):
        return {"id":e.id,"label":e.label,"description":e.description,"startDate":e.start_date,"endDate":e.end_date,"dataVersioning":e.data_versioning,"metadataVersion":e.metadata_version,"template":e.template,"status":e.status,"apiVisibility":e.api_visibility,"fields":e.fields,"actions":e.actions,"rules":e.rules,"createdAt":e.created_at,"updatedAt":e.updated_at}
    async def list(self): return [self.out(x) for x in (await self.db.scalars(select(MetadataEntity).order_by(MetadataEntity.updated_at.desc()))).all()]
    async def get_entity(self,id:UUID):
        e=await self.db.get(MetadataEntity,id)
        if not e: raise HTTPException(404,"Metadata not found")
        return e
    async def get(self,id): return self.out(await self.get_entity(id))
    async def create(self,m:MetadataCreate):
        d=m.model_dump(mode="json")
        e=MetadataEntity(label=d["label"],description=d["description"],start_date=d["startDate"],end_date=d["endDate"],data_versioning=d["dataVersioning"],metadata_version=d["metadataVersion"],template=d["template"],status=d["status"],api_visibility=d["apiVisibility"],fields=d["fields"],actions=d["actions"],rules=d["rules"])
        self.db.add(e); await self.db.commit(); await self.db.refresh(e); return self.out(e)
    async def update(self,id,m):
        e=await self.get_entity(id); d=m.model_dump(mode="json")
        for a,k in [("label","label"),("description","description"),("start_date","startDate"),("end_date","endDate"),("data_versioning","dataVersioning"),("template","template"),("status","status"),("api_visibility","apiVisibility"),("fields","fields"),("actions","actions"),("rules","rules")]: setattr(e,a,d[k])
        e.metadata_version=e.metadata_version+1 if e.data_versioning else d["metadataVersion"]
        await self.db.commit(); await self.db.refresh(e); return self.out(e)
    async def delete(self,id): e=await self.get_entity(id); await self.db.delete(e); await self.db.commit()
    async def submit(self,id,s,user):
        e=await self.get_entity(id); errors={}
        for f in e.fields:
            v=s.payload.get(f["name"])
            if f.get("required") and (v is None or v==""): errors[f["name"]]="Required"
            if v not in (None,"") and f["datatype"]=="NUMBER":
                try: float(v)
                except: errors[f["name"]]="Must be a number"
            if isinstance(v,str):
                if f.get("minLength") is not None and len(v)<f["minLength"]: errors[f["name"]]=f"Minimum length is {f['minLength']}"
                if f.get("maxLength") is not None and len(v)>f["maxLength"]: errors[f["name"]]=f"Maximum length is {f['maxLength']}"
        if errors: raise HTTPException(422,{"message":"Dynamic validation failed","fields":errors})
        row=SubmissionEntity(metadata_id=id,metadata_version=e.metadata_version,payload=s.payload,submitted_by=user.subject); self.db.add(row); await self.db.commit(); await self.db.refresh(row)
        return {"id":row.id,"metadataId":row.metadata_id,"metadataVersion":row.metadata_version,"payload":row.payload,"submittedBy":row.submitted_by,"submittedAt":row.submitted_at}
    async def options(self,id,field_name):
        e=await self.get_entity(id); f=next((x for x in e.fields if x["name"]==field_name),None)
        if not f: raise HTTPException(404,"Field not found")
        if f.get("options"): return f["options"]
        source=f.get("picklistDatasource")
        if not source: return []
        try: source_entity=await self.get_entity(UUID(source))
        except: raise HTTPException(400,"Invalid picklist datasource")
        key=f.get("picklistDatasourceField") or "label"
        rows=(await self.db.scalars(select(SubmissionEntity).where(SubmissionEntity.metadata_id==source_entity.id))).all()
        return [{"label":str(r.payload.get(key,"")),"value":r.payload.get(key)} for r in rows if r.payload.get(key) is not None]
