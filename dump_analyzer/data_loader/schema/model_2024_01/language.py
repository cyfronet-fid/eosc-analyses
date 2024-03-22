from typing import Optional

from pydantic import BaseModel, Field


class Language(BaseModel):
    code: Optional[str] = Field(
        None,
        description="Alpha-3/ISO 639-2 code of the language. Values controlled by the dnet:languages vocabulary.",
    )
    label: Optional[str] = Field(None, description="Language label in English.")
