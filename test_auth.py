from services.auth_service import (
    hash_password,
    verify_password
)

password = "fahad123"

hashed = hash_password(password)

print("Original:", password)
print("Hashed:", hashed)

print(
    verify_password(
        "fahad123",
        hashed
    )
)