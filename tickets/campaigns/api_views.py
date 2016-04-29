from restless.views import Endpoint


class HelloWorld(Endpoint):
    def get(self, request):
        name = request.params.get('name', 'World')
        return {'message': 'Hello, %s!' % name}

    def post(self, request):
        name = request.params.get('name', 'World')
        return {'message': 'POST Hello, %s!' % name}
