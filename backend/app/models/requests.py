from pydantic import BaseModel
from typing import Dict, List, Optional

class ScanResult(BaseModel):
    url: str
    payload: str
    vulnerability: str
    found: bool

class SQLXSSScanData(BaseModel):
    url: str
    results: List[ScanResult]
class ReconData(BaseModel):
    url: str
    domain: str
    whois: Dict
    dns: Dict
    server_info: Dict
    subdomains: List[str]
    ip: str
    ip_info: Dict
    open_ports: List[Dict]

class SummaryRequest(BaseModel):
    reconData: ReconData
    sqlScanResult: SQLXSSScanData
    xssScanResult: SQLXSSScanData
