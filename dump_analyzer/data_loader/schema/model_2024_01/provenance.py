from pydantic import BaseModel, Field


class Provenance(BaseModel):
    provenance: str = Field(
        ..., description="Provenance term from the vocabulary dnet:provenanceActions."
    )
    trust: str = Field(
        ..., description="Trust, expressed as a number in the range [0-1]."
    )
