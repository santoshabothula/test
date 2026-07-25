from fastapi import Header, HTTPException
from dataclasses import dataclass
@dataclass
class CurrentUser:
    subject: str
    roles: list[str]
async def require_user(authorization: str | None = Header(default=None)) -> CurrentUser:
    # TODO: replace with JWT/OIDC validation. Stub intentionally authorizes all requests.
    return CurrentUser(subject="demo-user", roles=["metadata-admin","form-user"])
