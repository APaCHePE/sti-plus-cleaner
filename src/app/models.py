from typing import Optional

from pydantic import BaseModel

class User(BaseModel):

    name: str
    email: str
    phone: Optional[str] = None
