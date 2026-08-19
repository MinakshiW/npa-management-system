from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken

class LogoutAPI(APIView):

    permission_classes = [IsAuthenticated]


    def post(self, request):

        refresh_token = request.data.get('refresh')

        if not RefreshToken:
            return Response(
                {
                    'error': 'Refresh token is required.'
                },
                status = status.HTTP_400_BAD_REQUEST
            )

        try:

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {
                    'message' : 'Successfully logged out..'
                },
                status=status.HTTP_200_OK
            )

        except Exception:

            return Response(
                {
                    'error' : 'Invalid or expired refresh token.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )