from enum import  Enum
from typing import List, Optional
from pydantic import BaseModel, Field

from cfhbkeyvalue import CfHbKeyValue
from pid import Pid


class OpenAccessRoute(Enum):
    gold = 'gold'
    green = 'green'
    hybrid = 'hybrid'
    bronze = 'bronze'


class Accessright(BaseModel):
    code: Optional[str] = Field(
        None,
        description="COAR access mode code: http://vocabularies.coar-repositories.org/documentation/access_rights/",
    )
    label: Optional[str] = Field(None, description="Label for the access mode.")
    openAccessRoute: Optional[OpenAccessRoute] = Field(
        None,
        description="Indicates the OpenAccess status. Values are set according to the Unpaywall methodology."
    )
    scheme: Optional[str] = Field(
        None,
        description="Scheme of reference for access right code. Always set to COAR access rights vocabulary: "
                    "http://vocabularies.coar-repositories.org/documentation/access_rights/"
    )


class Articleprocessingcharge(BaseModel):
    amount: Optional[str] = Field(None, description="The quantity of money.")
    currency: Optional[str] = Field(
        None,
        description="The system of money in which the amount is expressed (Euro, USD, etc).",
    )


class Measure(BaseModel):
    key: Optional[str] = Field(None, description="The measure (i.e. popularity).")
    value: Optional[str] = Field(None, description="The value for that measure.")


class Instance(BaseModel):
    accessright: Optional[Accessright] = Field(
        None,
        description="The accessRights for this materialization of the result.",
    )
    alternateIdentifier: Optional[List[Pid]] = Field(
        None,
        description="All the identifiers associated to the result other than the authoritative ones.",
    )
    articleprocessingcharge: Optional[Articleprocessingcharge] = Field(
        None,
        description="The money spent to make this book or article available in Open Access. "
                    "Source for this information is the OpenAPC initiative.",
    )
    collectedfrom: Optional[CfHbKeyValue] = Field(
        None,
        description="Information about the source from which the records has been collected.",
    )
    eoscDsId: Optional[List[Pid]] = Field(
        None,
        description="Eosc data source ID.",
    )
    fulltext: Optional[str] = Field(
        None,
        description="The direct link to the full-text as collected from the data source.",
    )
    hostedby: Optional[CfHbKeyValue] = Field(
        None,
        description="Information about the source from which the instance can be viewed or downloaded.",
    )
    license: Optional[str] = Field(
        None,
        description="The license URL.",
    )
    measures: Optional[List[Measure]] = Field(
        None,
        description="Measures computed for this instance, for example Bip!Finder ones",
    )
    pid: Optional[List[Pid]] = Field(
        None,
        description="The set of persistent identifiers associated to this instance that have been collected "
                    "from an authority for the pid type (i.e. Crossref/Datacite for doi)."
    )
    publicationdate: Optional[str] = Field(
        None,
        description="Date of the research product.",
    )
    refereed: Optional[str] = Field(
        None,
        description="If this instance has been peer-reviewed or not. Allowed values are peerReviewed, "
                    "nonPeerReviewed, UNKNOWN (as defined in https://api.openaire.eu/vocabularies/dnet:review_levels)",
    )
    type: Optional[str] = Field(
        None,
        description="The specific sub-type of this instance "
                    "(see https://api.openaire.eu/vocabularies/dnet:result_typologies following the links)",
    )
    url: Optional[List[str]] = Field(
        None,
        description="URLs to the instance. They may link to the actual full-text or to the landing page at the "
                    "hosting source.",
    )
