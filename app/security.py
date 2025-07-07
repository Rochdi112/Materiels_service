from fastapi import Depends, HTTPException, status

# ⚠️ Mock temporaire – à remplacer par appel JWT centralisé
def get_current_user():
    class User:
        role = "admin"
    return User()

def admin_required(current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
