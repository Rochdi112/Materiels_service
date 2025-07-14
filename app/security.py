from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from typing import Annotated
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer

# 🔐 Doit correspondre à ce qui est utilisé dans `auth_service`
SECRET_KEY = "secret"  # à remplacer par la même clé utilisée dans auth_service
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://auth_service/api/auth/login")

# ✅ Modèle d'utilisateur pour l'ERP
class TokenUser(BaseModel):
    id: int
    username: str
    role: str


# 🔍 Décodage du token JWT
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalide ou expiré",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        username: str = payload.get("username")
        role: str = payload.get("role")
        if not all([user_id, username, role]):
            raise credentials_exception
        return TokenUser(id=user_id, username=username, role=role)
    except JWTError:
        raise credentials_exception


# 📎 Typage standardisé pour toutes les routes
UserDep = Annotated[TokenUser, Depends(get_current_user)]


# 🔐 Vérification de rôle admin
def admin_required(current_user: UserDep) -> TokenUser:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Accès admin requis")
    return current_user


# 🛠️ Vérification technicien ou admin
def technicien_required(current_user: UserDep) -> TokenUser:
    if current_user.role not in ("admin", "technicien"):
        raise HTTPException(status_code=403, detail="Accès technicien ou admin requis")
    return current_user


# 🔍 Lecture seule autorisée pour tout utilisateur valide
def readonly_access(current_user: UserDep) -> TokenUser:
    return current_user
