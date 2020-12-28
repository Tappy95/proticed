# coding=utf-8
import base64
# token解析器, 暂时废弃
import jwt

import config


def verify_jwt(token, secret=None):
    """
    检验jwt
    :param token: jwt
    :param secret: 密钥
    :return: dict: payload
    """
    if not secret:
        secret = config.JWT_SECRET

    # payload = jwt.decode(token, secret, algorithm=['HS256'])
    try:
        payload = jwt.decode(token, secret, algorithm=['HS256'])
    except jwt.PyJWTError:
        payload = None

    return payload

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MDkxNzIyMTUsIlVzZXJJZCI6Ijk5OTk5IiwicmVmcmVzaF90b2tlbiI6M30.5-NFQH_eqk_un8IfqSdxApQIpS_uGoz6paEcTum19NA'
print(verify_jwt(token, 'refresh'))
# from authlib.jose import JsonWebToken
# jwt = JsonWebToken(['RS256'])
import json
from datetime import datetime

token = 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjBhOTY4YmFhNjJlOTkwMjlhOTczNDE1ODg3MDI5ZmJkIiwidHlwIjoiSldUIn0.eyJuYmYiOjE2MDkxNDAzNzQsImV4cCI6MTYwOTE3NjM3NCwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo1MDAxIiwiYXVkIjpbImh0dHA6Ly9sb2NhbGhvc3Q6NTAwMS9yZXNvdXJjZXMiLCJiYWlsdW5BcGkiXSwiY2xpZW50X2lkIjoiYmFpbHVuQ2xpZW50Iiwic3ViIjoi5p2O5b-X5rSqIiwiYXV0aF90aW1lIjoxNjA5MTQwMzc0LCJpZHAiOiJsb2NhbCIsIlVzZXJJZCI6Ijc0NCIsInN1Y2Vzc3MiOiJ0cnVlIiwiQ29tcGFueSI6IntcIklkXCI6MSxcIkNvbXBhbnlDb2RlXCI6XCJiYWlsdW5cIixcIkNvbXBhbnlOYW1lXCI6XCLlub_lt57nmb7kvKbkvpvlupTpk77np5HmioDmnInpmZDlhazlj7hcIn0iLCJBbGxDb21wYW55IjoiVHJ1ZSIsIlVzZXJDb2RlTmV3IjoiQkwwMDYzIiwiVXNlckNvZGUiOiJCTDAwNjMiLCJPYVVzZXJJZCI6Ijc0NCIsIkRlcGFydG1lbnQiOiJ7XCJEZXBhcnRtZW50SWRcIjozMDAsXCJOYW1lXCI6XCLkuJrliqHns7vnu5_mtYHnqIvnu4RcIixcIkNvZGVcIjpcIlwifSIsInNjb3BlIjpbIm9wZW5pZCIsInByb2ZpbGUiLCJiYWlsdW5BcGkiXSwiYW1yIjpbImN1c3RvbSJdfQ.H7tcjR2u3fg6HZm5XDaf4HCvIYU-rdIXsjY1g3dXifeJUjD-M0G5RQL0ZLxcOLxHWIdNk2F8SKM0pgaxY2x9oPk2HRMHvE6IGWGHMnINz33EomkBX92wZvjL9tE5g_LkgWAFYYeZCKu_sQ2m7VoHdqvnirboGIq79TvvCSmwvKELwDk02HDVx6givWhtgQxv0NUzvMbPXfhMz8FduWoOQEzOl47u391uhapFHov32Ye4ZCRdU7TfMDbk5Y6mUlYJs7-b6mHI0ghXhtwTV7MHpgsB7babny3oiZDI6vmCaDvYT-qP42TFKYTFKig0OVFkJERZkLBwL-tOGvlsDf7-BQ'
b = 'eyJuYmYiOjE2MDkxNDAzNzQsImV4cCI6MTYwOTE3NjM3NCwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo1MDAxIiwiYXVkIjpbImh0dHA6Ly9sb2NhbGhvc3Q6NTAwMS9yZXNvdXJjZXMiLCJiYWlsdW5BcGkiXSwiY2xpZW50X2lkIjoiYmFpbHVuQ2xpZW50Iiwic3ViIjoi5p2O5b-X5rSqIiwiYXV0aF90aW1lIjoxNjA5MTQwMzc0LCJpZHAiOiJsb2NhbCIsIlVzZXJJZCI6Ijc0NCIsInN1Y2Vzc3MiOiJ0cnVlIiwiQ29tcGFueSI6IntcIklkXCI6MSxcIkNvbXBhbnlDb2RlXCI6XCJiYWlsdW5cIixcIkNvbXBhbnlOYW1lXCI6XCLlub_lt57nmb7kvKbkvpvlupTpk77np5HmioDmnInpmZDlhazlj7hcIn0iLCJBbGxDb21wYW55IjoiVHJ1ZSIsIlVzZXJDb2RlTmV3IjoiQkwwMDYzIiwiVXNlckNvZGUiOiJCTDAwNjMiLCJPYVVzZXJJZCI6Ijc0NCIsIkRlcGFydG1lbnQiOiJ7XCJEZXBhcnRtZW50SWRcIjozMDAsXCJOYW1lXCI6XCLkuJrliqHns7vnu5_mtYHnqIvnu4RcIixcIkNvZGVcIjpcIlwifSIsInNjb3BlIjpbIm9wZW5pZCIsInByb2ZpbGUiLCJiYWlsdW5BcGkiXSwiYW1yIjpbImN1c3RvbSJdfQ'

# list1 = token.split('.')
# b_payload = list1[1]
# print(base64.b64decode(b).decode())
# print(i + '=' * (-len(i) % 4))
print()
# token = '123.123.123'
i = token.split('.')[1]
print(eval(base64.urlsafe_b64decode(i + '=' * (-len(i) % 4)).decode('UTF-8', "ignore")))
# print(datetime.utcnow().isoformat() + "Z")
# print(datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+"Z")
# print(base64.b64decode(i + '=' * (-len(i) % 4))[300:315])