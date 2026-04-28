import base64
import time
import traceback
import urllib.request

MAX_RETRIES = 5


def acl4ssr2autoproxy():
    url = "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/refs/heads/master/Clash/ChinaDomain.list"
    print(f"downloading from {url}")
    try_times = 0
    while try_times < MAX_RETRIES:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as response:
                acl4ssr = response.read().decode("utf-8")
            try_times = MAX_RETRIES + 1
        except:
            try_times += 1
            error = Exception(traceback.format_exc())
            print(f"{error}")
            time.sleep(try_times * 5)
    if try_times == MAX_RETRIES:
        print("convert failed")
        exit(-1)
    autoproxy_lines = ["[AutoProxy 0.2.9]", "! Title: ChinaDomain AutoProxy List", f"! Source: {url}", ""]
    for line in acl4ssr.splitlines():
        line = line.strip()
        if line.startswith("- "):
            line = line[2:].strip()
        if not line or line.startswith("#") or line.startswith("//"):
            continue
        rule_content = line.split("#")[0].split("//")[0].strip()
        parts = [p.strip() for p in rule_content.split(",")]
        if len(parts) >= 2:
            rule_type = parts[0].upper()
            payload = parts[1]
            if rule_type in ["DOMAIN-SUFFIX", "DOMAIN"]:
                autoproxy_lines.append(f"||{payload}")
            elif rule_type == "DOMAIN-KEYWORD":
                autoproxy_lines.append(payload)
    autoproxy = "\n".join(autoproxy_lines)
    filename = "ACL4SSR_ChinaDomain_AutoProxy.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(autoproxy)
    b64_filename = "ACL4SSR_ChinaDomain_AutoProxy_Base64.txt"
    with open(b64_filename, "w", encoding="utf-8") as f:
        f.write(base64.b64encode(autoproxy.encode("utf-8")).decode("utf-8"))
    print("")
    print("convert finished")


if __name__ == "__main__":
    acl4ssr2autoproxy()
