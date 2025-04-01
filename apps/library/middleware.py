import time

from commons.common import celery_logger
from django.utils.deprecation import MiddlewareMixin

logger = celery_logger


class RequestLoggingMiddleware(MiddlewareMixin):
    """记录每个 API 请求的参数和耗时"""

    def process_request(self, request):
        # 记录请求开始时间
        request.start_time = time.time()
        return None

    def process_response(self, request, response):
        # 计算请求处理耗时
        duration = time.time() - request.start_time
        # 记录请求的参数和耗时
        log_data = {
            'method': request.method,
            'path': request.path,
            'query_params': request.GET.dict(),  # 对于 GET 请求，记录查询参数
            'post_params': request.POST.dict(),  # 对于 POST 请求，记录 POST 数据
            'duration': duration,
            'response_status': response.status_code,
        }
        logger.info(log_data)
        return response
