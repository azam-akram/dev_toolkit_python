import jwt
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_public_key(public_key_file):
    """Load public key from file."""
    try:
        with open(public_key_file, "r") as f:
            return f.read()
    except FileNotFoundError:
        logging.error("Public key file not found.")
        return None

def verify_jwt(token, public_key_file):
    """Verify and decode JWT using an RSA public key."""
    public_key = load_public_key(public_key_file)
    if not public_key:
        return None

    try:
        decoded_payload = jwt.decode(token, public_key, algorithms=["RS256"], audience="www.example.com")
        logging.info("Decoded JWT Payload: %s", decoded_payload)
        return decoded_payload
    except jwt.ExpiredSignatureError:
        logging.error("JWT has expired.")
    except jwt.InvalidTokenError:
        logging.error("Invalid JWT.")
    except Exception as e:
        logging.error("Error verifying JWT: %s", str(e))

    return None

if __name__ == "__main__":
    public_key_path = f'C://Users/azam/python/github/dev_toolkit_python/jwt/public_key.pem'
    token = input("Enter JWT to verify: ")
    verify_jwt(token, public_key_path)
