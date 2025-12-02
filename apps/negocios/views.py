from rest_framework import viewsets
from .models import Negocios

from .serializers import NegociosSerializer
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

# Importar tu agente
from .agente5 import graph

class NegociosViewSet(viewsets.ModelViewSet):
    queryset = Negocios.objects.all()
    serializer_class = NegociosSerializer
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