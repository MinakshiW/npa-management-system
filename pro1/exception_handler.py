import logging

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is not None:

        logger.warning(
            'API Exception: %s',
            exc
        )

        return response

    logger.exception(
        'unexpected exception occurred...',
        exc_info=exc
    )

    return Response(
        {
            'error' : 'An unexpected error occured..',
            'detail' : 'Please try again later'
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )