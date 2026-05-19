import hashlib
import hmac
import json
import os
import urllib.request
from datetime import datetime, timezone

def main():
    name = os.environ["APPLICATION_NAME"]
    email = os.environ["APPLICATION_EMAIL"]
    resume_link = os.environ["APPLICATION_RESUME_LINK"]

    server_url = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
    repository = os.environ["GITHUB_REPOSITORY"]
    run_id = os.environ["GITHUB_RUN_ID"]

    repository_link = f"{server_url}/{repository}"
    action_run_link = f"{server_url}/{repository}/actions/runs/{run_id}"

    payload = dict(
        action_run_link=action_run_link,
        email=email,
        name=name,
        repository_link=repository_link,
        resume_link=resume_link,
        timestamp=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    )

    body = json.dumps(payload, separators=(",", ":"), ensure_ascii=True).encode("utf-8")

    secret = os.environ.get("APPLICATION_SIGNING_SECRET")
    digest = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()

    req = urllib.request.Request(
        "https://b12.io/apply/submission",
        data=body,
        headers={
            "X-Signature-256": f"sha256={digest}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(req) as resp:
        response = json.loads(resp.read().decode("utf-8"))
        print(response["receipt"])


if __name__ == "__main__":
    main()
