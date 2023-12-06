from typing import Optional

from pydantic import BaseModel, Field


class Subject(BaseModel):
    scheme: Optional[str] = Field(
        None,
        description="OpenAIRE subject classification scheme "
                    "(https://api.openaire.eu/vocabularies/dnet:subject_classification_typologies)."
    )
    value: Optional[str] = Field(
        None,
        description="The value for the subject in the selected scheme. When the scheme is 'keyword', "
                    "it means that the subject is free-text (i.e. not a term from a controlled vocabulary)."
    )