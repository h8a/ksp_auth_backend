from datetime import datetime, timedelta

import falcon
import jwt
import logging

from passlib.hash import pbkdf2_sha256

from db.models import UsersModel
from resources import BaseResource
from security.tokens import JWToken


class AuthRegisterResource(BaseResource):

    async def on_post(self, req, resp):
        data = await req.get_media()

        user_db = await UsersModel.get(self.db.session, username=data.get('username'))

        if user_db:
            resp.status = falcon.HTTP_400
            resp.media = {
                'status': False,
                'message': 'User already exists'
            }
            return

        users_model = UsersModel(
            username=data.get('username'),
            password=pbkdf2_sha256.hash(data.get('password'))
        )

        try:
            user_db = await users_model.save(self.db.session)
        except Exception:
            logging.getLogger('db').error('Error to try save user', exc_info=True)
            resp.status = falcon.HTTP_503
            resp.media = {
                'status': False,
                'message': 'Error to try save user'
            }
            return

        resp.status = falcon.HTTP_201
        resp.media = {
            'status': True,
            'data': {
                'id': str(user_db.id),
                'username': user_db.username
            }
        }


class AuthLoginResource(BaseResource):

    async def on_post(self, req, resp):
        data = await req.get_media()

        user_db = await UsersModel.get(self.db.session, username=data.get('username'), status='1')

        if not user_db:
            resp.status = falcon.HTTP_404
            resp.media = {
                'status': False,
                'message': 'User not found'
            }
            return

        if not pbkdf2_sha256.verify(data.get('password'), user_db.password):
            resp.status = falcon.HTTP_401
            resp.media = {
                'status': False,
                'message': 'Incorrecto user or password'
            }
            return

        try:
            token = JWToken.generate(
                payload={
                    'id': str(user_db.id),
                    'exp': datetime.utcnow() + timedelta(minutes=self.jwt_settings.exp_min),
                },
                secret=self.jwt_settings.secret,
                algorithm=self.jwt_settings.algorithm
            )
        except Exception:
            logging.getLogger('app').error('Error to try generate token', exc_info=True)
            resp.media = falcon.HTTP_503
            resp.media = {
                'status': False,
                'message': 'Error to try generate token'
            }
            return

        resp.status = falcon.HTTP_202
        resp.media = {
            'status': True,
            'data': {
                'username': user_db.username,
                'token': token
            }
        }


class ValidateJWTTokenResource(BaseResource):

    async def on_get(self, req, resp):
        header_token = req.get_header('Authorization')

        if not header_token:
            resp.status = falcon.HTTP_401
            resp.media = {
                'status': False,
                'message': 'Bad authorization header'
            }
            return

        token = self.__valid_header_structure(header_token=header_token)

        if not token:
            resp.status = falcon.HTTP_403
            resp.media = {
                'status': False,
                'message': 'Invalid structure token'
            }
            return

        try:
            token_decoded = jwt.decode(
                token,
                self.jwt_settings.secret,
                leeway=self.jwt_settings.leeway_sec,
                algorithms=[self.jwt_settings.algorithm]
            )
        except jwt.InvalidTokenError:
            resp.status = falcon.HTTP_403
            resp.media = {
                'status': False,
                'message': 'Unauthorization token'
            }
            return

        user_db = await UsersModel.get(self.db.session, id=str(token_decoded.get('id')))

        if not user_db:
            resp.status = falcon.HTTP_403
            resp.media = {
                'status': False,
                'message': 'Invalid user token'
            }
            return

        resp.status = falcon.HTTP_200
        resp.media = {
            'status': True,
            'data': {
                'id': str(token_decoded.get('id')),
                'username': user_db.username
            }
        }

    def __valid_header_structure(self, header_token):
        signature, token = header_token.split(' ')
        if signature != self.jwt_settings.signature:
            return False

        return token