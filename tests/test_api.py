import httpx
import json

BASE = "http://localhost:8000/api/v1"


def pretty(j):
    print(json.dumps(j, indent=2))


def run_tests():
    # Create
    payload = {
        "incident_type": "Test",
        "description": "This is a test incident",
        "location": "Unit Test",
        "date_time": "2025-11-08T12:00:00Z",
        "severity_level": "low",
        "contact_information": "tester@example.org",
    }

    with httpx.Client() as client:
        r = client.post(f"{BASE}/incidents/", json=payload, timeout=10.0)
        print("POST status:", r.status_code)
        pretty(r.json())
        created = r.json()

        incident_id = created.get("id")

        # Get
        r = client.get(f"{BASE}/incidents/{incident_id}")
        print("GET status:", r.status_code)
        pretty(r.json())

        # List
        r = client.get(f"{BASE}/incidents/")
        print("LIST status:", r.status_code)
        pretty(r.json())

        # Update
        update = {"severity_level": "moderate"}
        r = client.put(f"{BASE}/incidents/{incident_id}", json=update)
        print("PUT status:", r.status_code)
        pretty(r.json())

        # Delete
        r = client.delete(f"{BASE}/incidents/{incident_id}")
        print("DELETE status:", r.status_code)
        try:
            pretty(r.json())
        except Exception:
            print(r.text)


if __name__ == "__main__":
    run_tests()
