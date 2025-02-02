from pydantic import BaseModel
from typing import List

class ColorResponse(BaseModel):
    colors: List[str]
