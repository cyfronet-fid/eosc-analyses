from typing import List, Optional

from pydantic import BaseModel, Field

from affiliation import Affiliation
from author import Author
from bestaccessright import BestAccessRight
from cfhbkeyvalue import  CfHbKeyValue
from container import Container
from context import Context
from country import Country
from eosc_if import EoscIF
from geolocation import GeoLocation
from indicator import Indicator
from instance import Instance
from language import Language
from pid import Pid
from project import Project
from relation import Relation
from subject import Subject


class ResearchProduct(BaseModel):
    affiliation: Optional[List[Affiliation]] = Field(
        None,
        description='The list of organizations the result is affiliated to'
    )
    author: Optional[List[Author]] = Field(
        None,
        description="The main researchers involved in producing the data, or the authors of the publication."
    )
    bestaccessright: Optional[BestAccessRight] = Field(
        None,
        description='The openest of the access rights of this result.'
    )
    codeRepositoryUrl: Optional[str] = Field(
        None,
        description="Only for results with type 'software': the URL to the repository with the source code",
    )
    collectedfrom: Optional[List[CfHbKeyValue]] = Field(
        None,
        description="Information about the sources from which the result has been collected"
    )
    contactgroup: Optional[List[str]] = Field(
        None,
        description="Only for results with type 'software': Information on the group responsible for providing "
                    "further information regarding the resource",
    )
    contactperson: Optional[List[str]] = Field(
        None,
        description="Only for results with type 'software': Information on the person responsible for providing "
                    "further information regarding the resource",
    )
    container: Optional[Container] = Field(
        None,
        description="Container has information about the conference or journal where the result has been presented or "
                    "published",
    )
    context: Optional[List[Context]] = Field(
        None,
        description="Reference to a relevant research infrastructure, initiative or community (RI/RC) among those "
                    "collaborating with OpenAIRE. Please see https://connect.openaire.eu",
    )
    contributor: Optional[List[str]] = Field(
        None,
        description="Contributors for the result",
    )
    country: Optional[List[Country]] = Field(
        None,
        description="The list of countries associated to this result",
    )
    coverage: Optional[List[str]] = Field(
        None,
        description="",
    )
    dateofcollection: Optional[str] = Field(
        None,
        description="When OpenAIRE collected the record the last time",
    )
    description: Optional[List[str]] = Field(
        None,
        description="A brief description of the resource and the context in which the resource was created.",
    )
    documentationUrl: Optional[List[str]] = Field(
        None,
        description="Only for results with type 'software': URL to the software documentation",
    )
    embargoenddate: Optional[str] = Field(
        None,
        description="Date when the embargo ends and this result turns Open Access",
    )
    eoscif: Optional[List[EoscIF]] = Field(
        None,
        description="Describes a reference to the EOSC Interoperability Framework (IF) Guidelines",
    )
    format: Optional[List[str]] = Field(
        None,
        description="",
    )
    fulltext: Optional[List[str]] = Field(
        None,
        description="The direct link to the full-text as collected from the data source.",
    )
    geolocation: Optional[List[GeoLocation]] = Field(
        None,
        description="Geolocation information.",
    )
    id: str = Field(
        ...,
        description="The OpenAIRE identifier for this result."
    )
    indicator: Optional[Indicator] = Field(
        None,
        description="The indicators for this result.",
    )
    instance: Optional[List[Instance]] = Field(
        None,
        description="Specific materialization or version of the result. For example, you can have one result "
                    "with three instances: one is the pre-print, one is the post-print, one is the published version.",
    )
    keywords: Optional[List[str]] = Field(
        None,
        description="The list of keywords associated to the result.",
    )
    language: Optional[Language] = Field(
        None,
        description="Represents information for the language of the result.",
    )
    lastupdatetimestamp: Optional[int] = Field(
        None,
        description="Timestamp of last update of the record in OpenAIRE",
    )
    maintitle: Optional[str] = Field(
        None,
        description="A name or title by which a scientific result is known. May be the title of a publication, "
                    "of a dataset or the name of a piece of software.",
    )
    originalid: Optional[List[str]] = Field(
        None,
        description="Identifiers of the record at the original sources.",
    )
    pid: Optional[List[Pid]] = Field(
        None,
        description="Persistent identifiers of the result.",
    )
    programminglanguage: Optional[str] = Field(
        None,
        description="Only for results with type 'software': the programming language.",
    )
    projects: Optional[List[Project]] = Field(
        None,
        description="List of projects (i.e. grants) that (co-)funded the production ofn the research results.",
    )
    publicationdate: Optional[str] = Field(
        None,
        description="Main date of the research product: typically the publication or issued date. "
                    "In case of a research result with different versions with different dates, "
                    "the date of the result is selected as the most frequent well-formatted date. "
                    "If not available, then the most recent and complete date among those that are well-formatted. "
                    "For statistics, the year is extracted and the result is counted only among the result "
                    "of that year. Example: Pre-print date: 2019-02-03, Article date provided by repository: 2020-02, "
                    "Article date provided by Crossref: 2020, OpenAIRE will set as date 2019-02-03, "
                    "because it’s the most recent among the complete and well-formed dates. "
                    "If then the repository updates the metadata and set a complete date (e.g. 2020-02-12), "
                    "then this will be the new date for the result because it becomes the most recent "
                    "most complete date. However, if OpenAIRE then collects the pre-print from another repository "
                    "with date 2019-02-03, then this will be the “winning date” because it becomes the most frequent "
                    "well-formatted date.",
    )
    publisher: Optional[str] = Field(
        None,
        description="The name of the entity that holds, archives, publishes prints, distributes, releases, issues, "
                    "or produces the resource.",
    )
    relations: Optional[List[Relation]] = Field(
        None,
        description="The set of relations associated to this result."
    )
    size: Optional[str] = Field(
        None,
        description="Only for results with type 'dataset': the declared size of the dataset."
    )
    source: Optional[List[str]] = Field(
        None,
        description="See definition of Dublin Core field dc:source."
    )
    subject: Optional[List[Subject]] = Field(
        None,
        description="The subject dumped by type associated to the result."
    )
    subtitle: Optional[str] = Field(
        None,
        description="Explanatory or alternative name by which a scientific result is known."
    )
    tool: Optional[List[str]] = Field(
        None,
        description="Only for results with type 'other': tool useful for the interpretation and/or re-used of the "
                    "research product."
    )
    type: Optional[str] = Field(
        None,
        description="Type of the result: one of 'publication', 'dataset', 'software', 'other' (see also "
                    "https://api.openaire.eu/vocabularies/dnet:result_typologies)."
    )
    version: Optional[str] = Field(
        None,
        description="Version of the result."
    )
