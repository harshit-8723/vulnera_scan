from pydantic import BaseModel
from typing import Dict, List

class ScanResult(BaseModel):
    url: str
    urls : List[str] # reutrn all fetched urls
    vulnerabilities: Dict[str, List[str]]