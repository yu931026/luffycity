"""
响应的数据格式
"""


class BaseResponse(object):
    """
    数据类型
    ret = {"code":1000, "data": None, "error": None,}
    """

    def __init__(self):
        self.code = 1000
        self.data = None
        self.error = None

    @property
    def dict(self):  # 用于 Response时返回对象里面的值。
        return self.__dict__


class TokenResponse(BaseResponse):
    """
    数据类型
    ret = {"code":1000, "data": None, "error": None, "token": None}
    """

    def __init__(self):
        self.token = None
        super(TokenResponse, self).__init__()
