from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def admin_dependency(token: str = Security(oauth2_scheme)):
    # Logic to verify admin token
    if not token or token != "admin_token":
        raise HTTPException(status_code=403, detail="Not authorized")
    return True