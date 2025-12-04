from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from langchain_core.messages import HumanMessage
from .agent import focusbuddy_agent

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
