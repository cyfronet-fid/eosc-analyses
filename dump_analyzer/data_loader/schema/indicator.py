from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class BipIndicator(BaseModel):
    INDICATOR_CHOICES = Literal["influence", "influence_alt", "popularity", "popularity_alt", "impulse"]

    indicator: INDICATOR_CHOICES = Field(
        None,
        description="The name of indicator; it can be either one of:"
                    "influence, influence_alt, popularity, popularity_alt, impulse"
    )
    score: Optional[str] = Field(None, description="The actual indicator score.")
    class_: Optional[str] = Field(
        None,
        alias="class",
        description="The impact class assigned based on the indicator score."
    )


class UsageCounts(BaseModel):
    views: Optional[str] = Field(None, description="The number of views for this result.")
    downloads: Optional[str] = Field(None, description="The number of downloads for this result.")


class Indicator(BaseModel):
    bipIndicators: Optional[List[BipIndicator]] = Field(
        None,
        description="These impact-based indicators, provided by BIP!, estimate the impact of a result."
    )
    usageCounts: Optional[UsageCounts] = Field(
        None,
        description="These measures, computed by the UsageCounts Service, are based on usage statistics."
    )
