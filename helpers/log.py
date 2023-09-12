# 手动写日志
import logging

# django框架全局日志驱动
django_logger = logging.getLogger('django')

# django框架的request类别日志驱动
django_request_logger = logging.getLogger('django.request')

# 内容中间件工具默认日志驱动，存储位置为BASE_LOG_DIR/content_tools/下
logger = logging.getLogger('content_tools')
