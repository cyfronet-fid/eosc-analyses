from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from dump_analyzer.data_loader.schema.model_2024_01.provenance import Provenance


class SubjectEntry(BaseModel):
    provenance: Optional[Provenance] = Field(
        None, description="Contains provenance information for the subject term."
    )
    value: str = Field(
        ...,
        description="The value for the subject in the selected scheme. When the scheme is 'keyword', "
        "it means that the subject is free-text (i.e. not a term from a controlled vocabulary).",
    )


class Subject(BaseModel):
    subjects: Optional[Dict[str, List[SubjectEntry]]] = Field(
        None,
        description="OpenAIRE subject classification scheme "
        "(https://api.openaire.eu/vocabularies/dnet:subject_classification_typologies).",
    )
