from typing import List, Optional

from pydantic import BaseModel, Field


class Pid(BaseModel):
    scheme: Optional[str] = Field(
        None,
        description="The scheme of the persistent identifier for the result (i.e. doi).",
    )
    value: Optional[str] = Field(None, description="The value expressed in the scheme.")
