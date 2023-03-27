import jwt


class JWToken(object):

    def generate(payload, secret, algorithm):
        return jwt.encode(
            payload=payload,
            key=secret,
            algorithm=algorithm
        )