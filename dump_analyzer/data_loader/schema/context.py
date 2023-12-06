from typing import Optional, List
from pydantic import BaseModel, Field

from provenance import Provenance


class Context(BaseModel):
    code: Optional[str] = Field(None, description="Code identifying the RI/RC")
    label: Optional[str] = Field(None, description="Label of the RI/RC")
    provenance: Optional[List[Provenance]] = Field(
        None,
        description="Why this result is associated to the RI/RC."
    )