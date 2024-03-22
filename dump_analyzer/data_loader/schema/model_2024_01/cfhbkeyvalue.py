from pydantic import BaseModel, Field
from typing import Optional


class CfHbKeyValue(BaseModel):
    key: Optional[str] = Field(
        None, description="the OpenAIRE identifier of the data source"
    )
    value: Optional[str] = Field(None, description="the name of the data source")
