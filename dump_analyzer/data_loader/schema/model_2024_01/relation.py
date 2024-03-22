from typing import Optional
from pydantic import BaseModel, Field
from dump_analyzer.data_loader.schema.model_2024_01.provenance import Provenance


class Reltype(BaseModel):
    name: Optional[str] = Field(None, description="Name of the relation type.")
    type: Optional[str] = Field(None, description="Type of the relation.")


class Relation(BaseModel):
    provenance: Optional[Provenance] = Field(
        None,
        description="The reason why OpenAIRE holds the relation",
    )
    reltype: Optional[Reltype] = Field(
        None,
        description="To represent the semantics of a relation between two entities.",
    )
    source: Optional[str] = Field(
        None,
        description="The node source in the relation.",
    )
    target: Optional[str] = Field(
        None,
        description="The node target in the relation.",
    )
    targetType: Optional[str] = Field(
        None,
        description="Graph node type.",
    )
