from datetime import date, datetime
from enum import IntEnum, StrEnum
from typing import Any
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict, model_validator
class Status(IntEnum): ACTIVE=1; INACTIVE=2; HOLD=3; DRAFT=4
class ApiVisibility(IntEnum): ALLOW=1; NOT_ALLOWED=2
class DataType(StrEnum):
    NUMBER="NUMBER"; STRING="STRING"; DATE="DATE"; TIME="TIME"; DATETIME="DATETIME"; PICKLIST="PICKLIST"; USER="USER"; TRANSLATABLE="TRANSLATABLE"; BOOLEAN="BOOLEAN"
class Template(BaseModel):
    id: str|None=None
    label: str="Default template"
    description: str=""
    status: Status=Status.ACTIVE
    template: dict[str,Any]=Field(default_factory=lambda:{"layout":"single-column"})
class DynamicField(BaseModel):
    id: str
    name: str=Field(pattern=r"^[A-Za-z][A-Za-z0-9_]*$")
    label: str
    helpText: str=""
    defaultValue: Any=None
    datatype: DataType=DataType.STRING
    control: str="input"
    precision: int|None=Field(default=None, ge=0, le=15)
    trailingZeros: int|None=Field(default=None, ge=0, le=15)
    showSeconds: bool=False
    minLength: int|None=Field(default=None, ge=0)
    maxLength: int|None=Field(default=None, ge=1)
    picklistDatasource: str|None=None
    picklistDatasourceField: str|None=None
    picklistDatasourceFilterBy: list[str]=Field(default_factory=list)
    picklistDatasourceFormat: str|None=None
    options: list[dict[str,Any]]=Field(default_factory=list)
    includeInactiveUsers: bool=False
    country: list[str]=Field(default_factory=list)
    state: list[str]=Field(default_factory=list)
    required: bool=False
    showHistory: bool=False
    maskValueOnUi: bool=False
    @model_validator(mode="after")
    def validate_ranges(self):
        if self.minLength is not None and self.maxLength is not None and self.minLength>self.maxLength: raise ValueError("minLength cannot exceed maxLength")
        if self.datatype==DataType.PICKLIST and not (self.options or self.picklistDatasource): raise ValueError("PICKLIST requires options or picklistDatasource")
        return self
class MetadataBase(BaseModel):
    label: str=Field(min_length=1,max_length=200)
    description: str=""
    startDate: date|None=None
    endDate: date|None=None
    dataVersioning: bool=False
    metadataVersion: int=Field(default=1,ge=1)
    template: Template=Field(default_factory=Template)
    status: Status=Status.DRAFT
    apiVisibility: ApiVisibility=ApiVisibility.ALLOW
    fields: list[DynamicField]=Field(default_factory=list)
    actions: list[dict[str,Any]]=Field(default_factory=list)
    rules: list[dict[str,Any]]=Field(default_factory=list)
    @model_validator(mode="after")
    def validate_dates_names(self):
        if self.startDate and self.endDate and self.startDate>self.endDate: raise ValueError("startDate cannot be after endDate")
        names=[f.name for f in self.fields]
        if len(names)!=len(set(names)): raise ValueError("Field names must be unique")
        return self
class MetadataCreate(MetadataBase): pass
class MetadataRead(MetadataBase):
    id: UUID
    createdAt: datetime
    updatedAt: datetime
    model_config=ConfigDict(from_attributes=True)
class SubmissionCreate(BaseModel): payload: dict[str,Any]
class SubmissionRead(BaseModel):
    id: UUID; metadataId: UUID; metadataVersion: int; payload: dict[str,Any]; submittedBy: str; submittedAt: datetime
