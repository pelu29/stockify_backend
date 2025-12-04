from rest_framework import viewsets, status
from .models import Negocios
from .serializers import NegociosSerializer, InstructionSerializer, ResponseSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.agentes.agente_3 import process_instruction
# Create your views here.

class NegociosViewSet(viewsets.ModelViewSet):
    queryset = Negocios.objects.all()
    serializer_class = NegociosSerializer
    permission_classes = [IsAuthenticated]


class AgenteWellnessBot(viewsets.ModelViewSet):
    serializer_class = NegociosSerializer
    http_method_names = ["post"]
    def create(self, request, *args, **kwargs):
        serializer = InstructionSerializer(data=request.data)
        if serializer.is_valid():
            instruction = serializer.validated_data['instruction']

            try:
                agent_response = process_instruction(instruction)
            
            except Exception as e:
                return Response(str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            response = {"response" : agent_response}
            response_data = ResponseSerializer(data=response)
            if response_data.is_valid():
                return Response(response_data.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




