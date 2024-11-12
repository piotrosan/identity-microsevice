import jwt
import json

def create_hash(payload: dict, algorithm: str) -> str:
    alg_obj = jwt.get_algorithm_by_name(algorithm)
    return alg_obj.compute_hash_digest(
        json.dumps(payload).encode('UTF-8')
    )