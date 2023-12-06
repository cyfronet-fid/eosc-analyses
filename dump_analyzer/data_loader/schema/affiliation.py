from typing import List, Optional

from pydantic import BaseModel, Field


class AffiliationPid(BaseModel):
    type: Optional[str] = Field(None, description='the type of the organization pid')
    value: Optional[str] = Field(None, description='the value of the organization pid')


class Affiliation(BaseModel):
    id: Optional[str] = Field(None, description='the OpenAIRE id of the organization')
    name: Optional[str] = Field(None, description='the name of the organization')
    pid: Optional[List[AffiliationPid]] = Field(
        None, description='the list of pids we have in OpenAIRE for the oraganization'
    )
