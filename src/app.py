import falcon.asgi

from config import cfg
from db.manager import DBManager
from middleware.hooks import HookDBMiddleware
from resources.auth import AuthRegisterResource, AuthLoginResource, ValidateJWTTokenResource


class Service(falcon.asgi.App):

    def __init__(self, *args, **kwargs):
        super(Service, self).__init__(
            middleware=[
                HookDBMiddleware(cfg.db.connection)
            ],
            cors_enable=True
        )

        mgr = DBManager(cfg.db.connection)

        auth_res = AuthRegisterResource(db_manager=mgr, jwt=cfg.jwt)
        auth_login_res = AuthLoginResource(db_manager=mgr, jwt=cfg.jwt)
        auth_validate_token_res = ValidateJWTTokenResource(db_manager=mgr, jwt=cfg.jwt)

        self.add_route(f'/api/{cfg.api.version}/auth/register', auth_res)
        self.add_route(f'/api/{cfg.api.version}/auth/login', auth_login_res)
        self.add_route(f'/api/{cfg.api.version}/auth/token/validate', auth_validate_token_res)
