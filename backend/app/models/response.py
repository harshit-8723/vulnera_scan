from pydantic import BaseModel
from typing import Dict, List

class ScanResult(BaseModel):
    url: str
    vulnerabilities: Dict[str, List[str]]