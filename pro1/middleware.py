import logging
import time

logger = logging.getLogger(__name__)


class APILoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        start_time = time.time()

        response = self.get_response(request)

        execution_time = time.time() - start_time

        user = (
            request.user.username
            if request.user.is_authenticated
            else "Anonymous"
        )

        logger.info(
            "API Request | Method=%s | Path=%s | User=%s | "
            "Status=%s | Time=%.3fs",
            request.method,
            request.path,
            user,
            response.status_code,
            execution_time
        )

        return response