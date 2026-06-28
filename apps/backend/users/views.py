from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import AuthenticatedUserSerializer


class AuthMeView(APIView):
    """
    GET /api/v1/auth/me/

    Returns the locally synced profile for the authenticated Firebase user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = AuthenticatedUserSerializer(request.user)
        return Response(serializer.data)
