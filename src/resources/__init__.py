

class BaseResource(object):

    def __init__(self, db_manager, jwt=None):
        self.db = db_manager
        self.jwt_settings = jwt