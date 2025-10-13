from django.http import JsonResponse

def test_view(request):
    return JsonResponse({"mensaje": "Ruta de prueba funcionando"})
