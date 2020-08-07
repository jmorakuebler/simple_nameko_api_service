import json
from time import sleep
from nameko.web.handlers import HttpRequestHandler
from werkzeug.wrappers import Response
from nameko.exceptions import safe_for_serialization


class HttpError(Exception):
    error_code = 'BAD_REQUEST'
    status_code = 400


class InvalidArgumentsError(HttpError):
    error_code = 'INVALID_ARGUMENTS'


class HttpEntrypoint(HttpRequestHandler):
    def response_from_exception(self, exc):
        if isinstance(exc, HttpError):
            response = Response(
                json.dumps({
                    'error': exc.error_code,
                    'message': safe_for_serialization(exc),
                }),
                status=exc.status_code,
                mimetype='application/json'
            )
            return response
        return HttpRequestHandler.response_from_exception(self, exc)


def response_json_200(context):
    return Response(
        json.dumps(context),
        status=200,
        mimetype='application/json'
    )


class Service:
    name = "ExampleService"
    http = HttpEntrypoint.decorator

    @http('GET', '/hello_world')
    def hello_world(self, request):
        return 'Hello Word'

    @http('GET', '/greet_user/<string:user>')
    def greet_user(self, request, user):
        return response_json_200({'result': 'Oh, hi {}'.format(user.capitalize())})

    @http('POST', '/create_user')
    def create_user_mock(self, request):
        data = json.loads(request.get_data(as_text=True))
        username = data.get('username', None)
        if username is None:
            raise InvalidArgumentsError(400, "Value 'username' not sent")
        print("Mocking user creation")
        sleep(3)
        print("User created")
        return response_json_200({'result': 'User {} created'.format(username)})
