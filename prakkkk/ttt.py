import jwt as jwt

a = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTU1NjczMDgsIkFjY291bnQiOiJcdTViOGJcdTU5NTVcdThkMjQiLCJVc2VySWQiOjEyNjUyNTQ2Nzg2MTUxNjY5NzZ9.LPxBkJYdICJGNa5pH3mlv392NKBwp9KfyKmoOweyHYQ"
def verify_jwt(token, secret=None):
    """
    检验jwt
    :param token: jwt
    :param secret: 密钥
    :return: dict: payload
    """
    if not secret:
        secret = "secret"

    # payload = jwt.decode(token, secret, algorithm=['HS256'])
    try:
        payload = jwt.decode(token, secret, algorithm=['HS256'])
    except jwt.PyJWTError:
        payload = None

    return payload

print(verify_jwt(a))