from pydantic import BaseModel, Field
from typing import Optional


class EoscIF(BaseModel):
    code: Optional[str] = Field(None, description="EOSC code")
    label: Optional[str] = Field(None, description="EOSC label")
    semanticRelation: Optional[str] = Field(None, description="Semantic Relation")
    url: Optional[str] = Field(None, description="url")
