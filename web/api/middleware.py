from django.http import JsonResponse
from django.conf import settings

class APITokenMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    if request.path.startswith('/api'):
      token = request.headers.get('Webhook-Token')
      if token != settings.WEBHOOK_TOKEN:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    return self.get_response(request)