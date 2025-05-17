from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

#injects_payload to the url 
def inject_payload(url: str, payload: str) -> str:
    parsed = urlparse(url)
    
    #preserve empty values using `keep_blank_values=True`
    query = parse_qs(parsed.query, keep_blank_values=True)
    injected_query = {k: [v[0] + payload if v and v[0] else payload] for k, v in query.items()}
    new_query = urlencode(injected_query, doseq=True)
    
    return urlunparse(parsed._replace(query=new_query))
