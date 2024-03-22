from typing import Optional

from pydantic import BaseModel, Field

from dump_analyzer.data_loader.schema.model_2024_01.provenance import Provenance


class Country(BaseModel):
    code: Optional[str] = Field(None, description="ISO 3166-1 alpha-2 country code.")
    label: Optional[str] = Field(None, description="The country label.")
    provenance: Optional[Provenance] = Field(
        None,
        description="Indicates the reason why this country is associated to this result.",
    )
