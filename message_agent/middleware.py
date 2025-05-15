from django.utils import translation

class RelayLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        translation.deactivate()
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        language_code = view_kwargs.get('language_code')
        if language_code:
            translation.activate(language_code)
            request.LANGUAGE_CODE = language_code
