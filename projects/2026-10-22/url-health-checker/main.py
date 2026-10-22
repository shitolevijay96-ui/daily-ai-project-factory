import urllib.request
import urllib.error

DEFAULT_URLS = [
    "https://www.python.org",
    "https://httpbin.org/status/200",
    "https://httpbin.org/status/404"
]

def check_url(url):
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'URL-Health-Checker/1.0'}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            return {"url": url, "status": response.status, "ok": True}
    except urllib.error.HTTPError as e:
        return {"url": url, "status": e.code, "ok": False}
    except Exception as e:
        return {"url": url, "status": str(e), "ok": False}

def check_all(urls=None):
    if urls is None:
        urls = DEFAULT_URLS
    results = []
    for u in urls:
        results.append(check_url(u))
    return results

def main():
    print("Running URL health checks...")
    results = check_all()
    for res in results:
        status_label = "UP" if res["ok"] else "DOWN"
        print(f"[{status_label}] {res['url']} -> Status: {res['status']}")

if __name__ == "__main__":
    main()