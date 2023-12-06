from typing import Optional

from pydantic import BaseModel, Field


class Cointainer(BaseModel):
    name: Optional[str] = Field(None, description='Name of the journal or conference.')
    issnPrinted: Optional[str] = Field(None, description='The journal printed issn.')
    issnOnline: Optional[str] = Field(None, description='The journal online issn.')
    issnLinking: Optional[str] = Field(None, description='The journal linking issn.')
    iss: Optional[str] = Field(None, description='The journal issue.')
    sp: Optional[str] = Field(None, description='The start page.')
    ep: Optional[str] = Field(None, description='The end page.')
    vol: Optional[str] = Field(None, description='The journal volume.')
    edition: Optional[str] = Field(
        None, description='The edition of the journal or conference.'
    )
    conferenceplace: Optional[str] = Field(None, description="The place of the conference.")
    conferencedate: Optional[str] = Field(None, description="The date of the conference.")
