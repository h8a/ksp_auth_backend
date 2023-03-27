import aumbry
import os
from aumbry import Attr, YamlConfig


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class DatabaseConfig(YamlConfig):
    __mapping__ = {
        'connection': Attr('connection', str),
    }

    connection = os.getenv('DB', 'sqlite+aiosqlite:///:memory:')


class ServiceConfig(YamlConfig):
    __mapping__ = {
        'host': Attr('host', str),
        'port': Attr('port', int),
        'log_level': Attr('log_level', str),
        'debug': Attr('debug', bool),
    }

    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    log_level = os.getenv('LOG_LEVEL', 'info')
    debug = bool(os.getenv('DEBUG', True))


class JwtConfig(YamlConfig):
    __mapping__ = {
        'secret': Attr('secret', str),
        'exp_min': Attr('exp_min', int),
        'leeway_sec': Attr('leeway_sec', int),
        'algorithm': Attr('algorithm', str),
        'signature': Attr('signature', str),
    }

    secret = os.getenv('JWT_SECRET', 'topsecret')
    exp_min = int(os.getenv('JWT_EXP_MIN', 30))
    leeway_sec = int(os.getenv('JWT_LEEWAY', 10))
    algorithm = os.getenv('JWT_ALGORITHM', 'HS256')
    signature = os.getenv('JWT_SIGNATURE', 'Bearer')


class ApiConfig(YamlConfig):
    __mapping__ = {
        'version': Attr('version', str),
    }

    version = os.getenv('API_VERSION', 'v1.0.0')


class AppConfig(YamlConfig):
    __mapping__ = {
        'db': Attr('db', DatabaseConfig),
        'service': Attr('service', ServiceConfig),
        'api': Attr('api', ApiConfig),
        'jwt': Attr('jwt', JwtConfig)
    }

    def __init__(self):
        self.db = DatabaseConfig()
        self.service = ServiceConfig()
        self.api = ApiConfig()
        self.jwt = JwtConfig()


cfg = aumbry.load(
    aumbry.FILE,
    AppConfig,
    {
        'CONFIG_FILE_PATH': os.path.join(BASE_DIR, 'settings.yml'),
    }
)
