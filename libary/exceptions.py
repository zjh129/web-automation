class ActionException(Exception):
    # 未知错误码
    CODE_UNKNOWN_ERROR = 2001000
    CODE_PARAM_MISSING = 2001001
    CODE_COOKIE_EMPTY = 2001002
    CODE_COOKIE_EXPIRED = 2001003
    CODE_USER_ID_EMPTY = 2001004
    # 手机号码相关错误码
    CODE_PHONE_NUMBER_EMPTY = 2002001
    CODE_PHONE_INCORRECT = 2002002

    # 登录相关错误码
    CODE_VERIFY_CODE_EMPTY = 2003001
    CODE_VERIFY_CODE_INCORRECT = 2003002
    CODE_LOGIN_ERROR = 2003003
    CODE_VERIFY_TOO_MANY_TIMES = 2003004
    CODE_VERIFY_SERVICE_ERROR = 2003005
    CODE_PASSWORD_EMPTY = 2003006
    CODE_NOT_LOGIN = 2003007

    # 获取用户信息失败错误码
    CODE_GET_USER_INFO_ERROR = 2004001

    # 发布笔记错误码
    CODE_SEND_NOTE_ERROR = 2005001
    CODE_NOTE_TYPE_ERROR = 2005002
    CODE_FILE_LIST_EMPTY = 2005003
    CODE_DESCRIPTION_EMPTY = 2005004

    # 获取笔记错误码
    CODE_NOTE_EMPTY = 2006001
    CODE_NOTE_LIST_EMPTY = 2006002

    # 抖音视频号错误码
    CODE_DOUYIN_VIDEO_FILE_DOWNLOAD_ERROR = 2007001
    CODE_DOUYIN_VIDEO_CHECK_ERROR = 2007002
    CODE_DOUYIN_VIDEO_COVER_DOWNLOAD_ERROR = 2007003
    CODE_DOUYIN_VIDEO_COVER_UPLOAD_ERROR = 2007004
    CODE_DOUYIN_PUBLISH_TIME_ERROR = 2007005
    CODE_DOUYIN_IMAGE_LIST_EMPTY = 2007006
    CODE_DOUYIN_FILE_LIST_EMPTY = 2007007
    CODE_DOUYIN_DESCRIPTION_EMPTY = 2007008
    CODE_DOUYIN_DATA_LIST_ERROR = 2007009

    # 错误码与错误信息的映射
    CODE_MESSAGE_MAP = {
        CODE_UNKNOWN_ERROR: "未知错误",
        CODE_PARAM_MISSING: "缺少必填参数",
        CODE_COOKIE_EMPTY: "Cookie不能为空",
        CODE_COOKIE_EXPIRED: "Cookie已过期",
        CODE_USER_ID_EMPTY: "用户标识不能为空，不同用户登录信息将会隔离",

        CODE_PHONE_NUMBER_EMPTY: "手机号不能为空",
        CODE_PHONE_INCORRECT: "手机号格式不正确",

        # 登录相关错误码
        CODE_VERIFY_CODE_EMPTY: "验证码不能为空",
        CODE_VERIFY_CODE_INCORRECT: "验证码格式不正确",
        CODE_LOGIN_ERROR: "登录失败",
        CODE_VERIFY_TOO_MANY_TIMES: "验证码获取次数过多",
        CODE_VERIFY_SERVICE_ERROR: "验证码平台解码服务异常",
        CODE_PASSWORD_EMPTY: "密码不能为空",
        CODE_NOT_LOGIN: "未登录",

        CODE_GET_USER_INFO_ERROR: "获取用户信息失败",

        CODE_SEND_NOTE_ERROR: "发布笔记失败",
        CODE_NOTE_TYPE_ERROR: "笔记类型错误",
        CODE_FILE_LIST_EMPTY: "文件列表不能为空",
        CODE_DESCRIPTION_EMPTY: "作品描述不能为空",

        CODE_NOTE_EMPTY: "笔记列表获取失败",
        CODE_NOTE_LIST_EMPTY: "笔记列表为空",

        # 抖音视频号错误
        CODE_DOUYIN_VIDEO_FILE_DOWNLOAD_ERROR: "下载视频失败",
        CODE_DOUYIN_VIDEO_CHECK_ERROR: "视频检测失败",
        CODE_DOUYIN_VIDEO_COVER_DOWNLOAD_ERROR: "下载封面失败",
        CODE_DOUYIN_VIDEO_COVER_UPLOAD_ERROR: "上传封面失败",
        CODE_DOUYIN_PUBLISH_TIME_ERROR: "发布时间错误",
        CODE_DOUYIN_IMAGE_LIST_EMPTY: "图片列表不能为空",
        CODE_DOUYIN_FILE_LIST_EMPTY: "文件列表不能为空",
        CODE_DOUYIN_DESCRIPTION_EMPTY: "作品描述不能为空",
        CODE_DOUYIN_DATA_LIST_ERROR: "数据列表错误",
    }

    def __init__(self, code, custom_message=None):
        if code not in self.CODE_MESSAGE_MAP and custom_message is None:
            raise ValueError('无效的错误码并且未提供自定义消息')
        if custom_message is not None:
            self.message = custom_message
        else:
            self.message = self.CODE_MESSAGE_MAP.get(code, custom_message)
        super().__init__(self.message)
        self.code = code
