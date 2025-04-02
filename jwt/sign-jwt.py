import jwt
import logging
from datetime import datetime, timezone, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_private_key(private_key_file):
    """Load private key from file."""
    try:
        with open(private_key_file, "r") as f:
            return f.read()
    except FileNotFoundError:
        logging.error("Private key file not found.")
        return None

def generate_jwt(private_key_file):
    """Generate JWT signed with an RSA private key."""
    private_key = load_private_key(private_key_file)
    if not private_key:
        return None

    header = {
        "alg": "RS256",
        "typ": "JWT",
        "kid": "kid-123"
    }

    payload = {
        "exp": int((datetime.now(timezone.utc) + timedelta(days=1)).timestamp()),
        "iat": int(datetime.now(timezone.utc).timestamp()),
        "aud": "www.example.com",
        "iss": "issuer",
        "sub": "subject"
    }

    try:
        token = jwt.encode(payload, private_key, algorithm="RS256", headers=header)
        logging.info("Generated JWT: %s", token)
        return token
    except Exception as e:
        logging.error("Error generating JWT: %s", str(e))
        return None

if __name__ == "__main__":
    private_key_path = f'C://Users/azam/python/github/dev_toolkit_python/jwt/private_key.pem'
    jwt_token = generate_jwt(private_key_path)
