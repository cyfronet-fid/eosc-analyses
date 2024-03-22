from typing import List, Optional

from pydantic import BaseModel, Field


class BestAccessRight(BaseModel):
    code: Optional[str] = Field(
        None,
        description="COAR access mode code: http://vocabularies.coar-repositories.org/documentation/access_rights/",
    )
    label: Optional[str] = Field(None, description="Label for the access mode")
    scheme: Optional[str] = Field(
        None,
        description="Scheme of reference for access right code. Always set to COAR access rights vocabulary: "
        "http://vocabularies.coar-repositories.org/documentation/access_rights/",
    )
