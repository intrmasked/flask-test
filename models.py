from pydantic import BaseModel
from typing import List

class NamedUrls(BaseModel):
    name:str
    url:str



class PositionInfo(BaseModel):
    company:str
    position:str
    name:str
    blog_articles:List[str]


class PositionInfoList(BaseModel):
    positions:List[PositionInfo]
