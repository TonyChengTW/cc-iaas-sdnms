class BaseResource(object):

    def __init__(self, db_manager):
        self.db = db_manager
        self.result = {
            "status": 0,
            "error_msg": "",
            "content": {}
        }

    def set_result(self, status, error_msg, content):
        self.result["status"] = status
        self.result["error_msg"] = error_msg
        self.result["content"] = content

    def get_result(self):
        return self.result
