from pydantic import BaseModel, Field
from typing import Optional

from provenance import Provenance
from pid import Pid


class AuthorPid(BaseModel):
    id: Pid = Field(None, description="Type used to represent the scheme and value for the author's pid.")
    provenance: Provenance = Field(None, description="The reason why the pid was associated to the author.")


class Author(BaseModel):
    fullname: Optional[str] = Field(None, description="Author's full name.")
    name: Optional[str] = Field(None, description="Author's given name.")
    surname: Optional[str] = Field(None, description="Author's family name.")
    rank: Optional[str] = Field(None, description="Author's order in the list of authors for the given result.")
    pid: Optional[AuthorPid] = Field(None, description="Persistent identifier associated with this author.")
