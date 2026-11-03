from django.conf import settings
from django.http import HttpResponse


class MaintenanceModeMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if settings.MAINTENANCE_MODE:

            if request.path == '/admin' or request.path.startswith('/admin/'):
                return self.get_response(request)

            return HttpResponse(
                "Site is under maintenance",
                status=503
            )

        response = self.get_response(request)

        return response