def main():
import json
import requests

def main():
    url = "http://127.0.0.1:8000/domain"
    payload = {"target": "example.com", "all": True}
    try:
        r = requests.post(url, json=payload, timeout=20)
        print("Status:", r.status_code)
        try:
            print(json.dumps(r.json(), indent=2))
        except Exception:
            print(r.text)
    except Exception as e:
        print("Request failed:", e)


if __name__ == "__main__":
    main()
