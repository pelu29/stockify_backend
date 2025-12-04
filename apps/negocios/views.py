from rest_framework import viewsets, status
from .models import Negocios
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from langchain_core.messages import HumanMessage
from .agents import focusbuddy_agent

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .serializers import NegociosSerializer, InstructionSerializer, ResponseSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.agentes.agente_3 import process_instruction
# Create your views here.

# Importar tu agente
from .agente5 import graph

class NegociosViewSet(viewsets.ModelViewSet):
    queryset = Negocios.objects.all()
    serializer_class = NegociosSerializer



class FocusBuddyView(APIView):
    def post(self, request):
        user_input = request.data.get("message")
        if not user_input:
            return Response({"error": "Falta el campo 'message'"}, status=status.HTTP_400_BAD_REQUEST)

        respuesta = focusbuddy_agent.invoke(
            {"messages": [HumanMessage(content=user_input)]},
            config={"configurable": {"thread_id": "session_1"}}
        )

        output = [msg.content for msg in respuesta["messages"]]
        return Response({"reply": output})

    permission_classes = [IsAuthenticated]

@csrf_exempt
def ejecutar_agente(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido. Usa POST."}, status=405)

    try:
        body = json.loads(request.body)
        user_message = body.get("message", "").strip()

        if not user_message:
            return JsonResponse({"error": "Falta el campo 'message'."}, status=400)

        mensajes = [{"role": "user", "content": user_message}]

        # Ejecutar workflow del agente
        respuesta = graph.invoke(
            {"messages": mensajes},
            {"configurable": {"thread_id": "negocios"}}
        )

        contenido = respuesta["messages"][-1].content

        return JsonResponse({"response": contenido}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

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



