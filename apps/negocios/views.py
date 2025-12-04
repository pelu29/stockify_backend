from rest_framework import viewsets
from .models import Negocios
from .serializers import NegociosSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .chef_ai_agent import interactuar_con_chefai


# Create your views here.

class NegociosViewSet(viewsets.ModelViewSet):
    queryset = Negocios.objects.all()
    serializer_class = NegociosSerializer
    permission_classes = [IsAuthenticated]

class ChefAIAgentView(APIView):
    def post(self, request, *args, **kwargs):
        user_message = request.data.get("message")
        if not user_message:
            return Response(
                {"error": "El campo 'message' es requerido."},
                status=status.HTTP_400_BAD_REQUEST
            )

        thread_id = "chef_ai_session_web"

        try:
            agent_response = interactuar_con_chefai(user_message, thread_id)
            return Response({"response": agent_response}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Ocurrió un error al interactuar con ChefAI: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
