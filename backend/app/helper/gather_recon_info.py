import asyncio
import socket
from urllib.parse import urlparse
import whois
import dns.resolver
import httpx
import ssl
import json


# Extract domain and IP
def extract_domain_ip(url: str):
    parsed = urlparse(url)
    domain = parsed.netloc or parsed.path
    if ":" in domain:
        domain = domain.split(":")[0]
    ip = None
    try:
        ip = socket.gethostbyname(domain)
    except Exception:
        pass
    return domain, ip


# WHOIS lookup
async def perform_whois_lookup(domain: str):
    try:
        data = whois.whois(domain)
        return {
            "domain_name": data.domain_name,
            "registrar": data.registrar,
            "creation_date": str(data.creation_date),
            "expiration_date": str(data.expiration_date)
        }
    except Exception as e:
        return {"error": f"WHOIS lookup failed: {str(e)}"}


# DNS records
async def perform_dns_lookup(domain: str):
    records = {}
    try:
        for record_type in ["A", "AAAA", "MX", "NS", "TXT"]:
            answers = dns.resolver.resolve(domain, record_type, raise_on_no_answer=False)
            records[record_type] = [r.to_text() for r in answers] if answers else []
        return records
    except Exception as e:
        return {"error": f"DNS lookup failed: {str(e)}"}


# Real IP geolocation using ip-api.com
async def perform_ip_lookup(ip: str):
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(f"http://ip-api.com/json/{ip}")
            data = r.json()
            return {
                "ip": ip,
                "country": data.get("country"),
                "region": data.get("regionName"),
                "city": data.get("city"),
                "org": data.get("org"),
                "asn": data.get("as"),
                "isp": data.get("isp")
            }
    except Exception as e:
        return {"error": f"IP info lookup failed: {str(e)}"}


# Server headers
async def get_server_info(url: str):
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(url, timeout=10)
            return {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "server": response.headers.get("server", "Unknown")
            }
    except Exception as e:
        return {"error": f"Server info fetch failed: {str(e)}"}


# Live subdomain scan using crt.sh
async def find_subdomains(domain: str):
    try:
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10)
            subdomains = set()
            if response.status_code == 200:
                certs = response.json()
                for cert in certs:
                    name = cert.get("name_value")
                    if name:
                        for entry in name.splitlines():
                            if entry.endswith(domain):
                                subdomains.add(entry.strip())
            return sorted(subdomains)
    except Exception as e:
        return {"error": f"Subdomain enumeration failed: {str(e)}"}


# Port scan with banner grabbing
async def scan_ports(ip: str, ports=list(range(1, 1025))):
    open_ports = []

    def grab_banner(ip, port):
        try:
            s = socket.create_connection((ip, port), timeout=2)
            s.settimeout(2)
            try:
                banner = s.recv(1024).decode().strip()
            except:
                banner = "No banner"
            s.close()
            return port, banner
        except:
            return None

    loop = asyncio.get_event_loop()
    tasks = [loop.run_in_executor(None, grab_banner, ip, port) for port in ports]
    results = await asyncio.gather(*tasks)

    for result in results:
        if result:
            port, banner = result
            open_ports.append({"port": port, "banner": banner})

    return open_ports


# Aggregator
async def gather_recon_info(url: str):
    domain, ip = extract_domain_ip(url)
    if not domain:
        raise ValueError("Invalid URL")

    results = {"domain": domain, "url": url}

    whois_task = perform_whois_lookup(domain)
    dns_task = perform_dns_lookup(domain)
    server_info_task = get_server_info(url)
    subdomains_task = find_subdomains(domain)
    ip_info_task = perform_ip_lookup(ip) if ip else None
    ports_task = scan_ports(ip) if ip else None

    whois_res, dns_res, server_res, subdomains_res = await asyncio.gather(
        whois_task, dns_task, server_info_task, subdomains_task
    )

    results["whois"] = whois_res
    results["dns"] = dns_res
    results["server_info"] = server_res
    results["subdomains"] = subdomains_res

    if ip:
        results["ip"] = ip
        if ip_info_task:
            results["ip_info"] = await ip_info_task
        if ports_task:
            results["open_ports"] = await ports_task
    else:
        results["ip"] = None

    return results



# import asyncio
# import json

# if __name__ == "__main__":
#     test_url = "https://en.wikipedia.org/wiki/Website"  # 

#     async def main():
#         result = await gather_recon_info(test_url)
#         print(json.dumps(result, indent=4))

#     asyncio.run(main())