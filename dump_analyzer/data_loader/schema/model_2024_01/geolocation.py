from typing import Optional

from pydantic import BaseModel, Field


class GeoLocation(BaseModel):
    point: Optional[str] = Field(
        None, description="A point with Latitude and Longitude."
    )
    box: Optional[str] = Field(
        None,
        description="A specified bounding box defined by two longitudes (min and max) and two latitudes (min and max).",
    )
    place: Optional[str] = Field(None, description="The name of a specific place.")
