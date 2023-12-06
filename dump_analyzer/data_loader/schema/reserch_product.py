from typing import List, Optional

from pydantic import BaseModel, Field

from affiliation import Affiliation
from bestaccessright import BestAccessRight
from author import Author


class ResearchProduct(BaseModel):
    affiliation: Optional[List[Affiliation]] = Field(
        None, description='The list of organizations the result is affiliated to'
    )
    author: Optional[List[Author]] = Field(
        None, description="The main researchers involved in producing the data, or the authors of the publication."
    )
    bestaccessright: Optional[BestAccessRight] = Field(
        None, description='The openest of the access rights of this result.'
    )
    codeRepositoryUrl: Optional[str] = Field(
        None, description="Only for results with type 'software': the URL to the repository with the source code",
    )
    collectedfrom: Optional[List[dict]] = Field(
        None, description="Information about the sources from which the result has been collected"
    )
    contactgroup: Optional[List[dict]]
    contactperson: Optional[List[dict]]
    container: Optional[List[dict]]
    context: Optional[List[dict]]
    contributor: Optional[List[str]]
    country: Optional[List[dict]]
    coverage: Optional[List[str]]
    dateofcollection: Optional[str]
    description: Optional[List[str]]
    documentationurl: Optional[List[str]]
    embargoenddate: Optional[str]
    eoscif: Optional[List[dict]]
    format: Optional[List[str]]
    fulltext: Optional[List[str]]
    geolocation: Optional[List[dict]]
    id: str
    indicator: Optional[List[dict]]
    instance: Optional[List[dict]]
    keywords: Optional[List[dict]]
    language: Optional[List[dict]]
    lastupdatetimestamp: Optional[int]
    maintitle: Optional[str]
    originalid: Optional[List[str]]
    pid: Optional[List[dict]]
    programminglanguage: Optional[str]
    projects: Optional[List[dict]]
    publicationdate: Optional[str]
    publisher: Optional[str]
    relations: Optional[List[dict]]
    size: Optional[str]
    source: Optional[List[str]]
    subject: Optional[List[str]]
    subtitle: Optional[str]
    tool: Optional[List[str]]
    type: Optional[str]
    version: Optional[str ]


