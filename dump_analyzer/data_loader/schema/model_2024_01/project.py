from typing import Optional
from pydantic import BaseModel, Field

from dump_analyzer.data_loader.schema.model_2024_01.provenance import Provenance


class Funder(BaseModel):
    fundingStream: Optional[str] = Field(
        None,
        description="Stream of funding (e.g. for European Commission can be H2020 or FP7)",
    )
    jurisdiction: Optional[str] = Field(
        None,
        description="Geographical jurisdiction (e.g. for European Commission is EU, for Croatian Science Foundation "
        "is HR)",
    )
    name: Optional[str] = Field(
        None, description="The name of the funder (European Commission)"
    )
    shortName: Optional[str] = Field(
        None, description="The short name of the funder (EC)"
    )


class Validated(BaseModel):
    validatedByFunder: Optional[bool] = Field(
        None, description="Is validated by funder"
    )
    validationDate: Optional[str] = Field(None, description="Validation date.")


class Project(BaseModel):
    acronym: Optional[str] = Field(None, description="The acronym of the project")
    code: Optional[str] = Field(None, description="The grant agreement number")
    funder: Optional[Funder] = Field(
        None, description="Information about the funder funding the project"
    )
    id: Optional[str] = Field(None, description="The OpenAIRE id for the project")
    provenance: Optional[Provenance] = Field(
        None, description="Why this result is associated with Project"
    )
    title: Optional[str] = Field(None, description="The title of the project")
    validated: Optional[Validated] = Field(
        None, description="Is the Project validated by funder"
    )
