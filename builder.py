import json
import os
from pathlib import Path

from flask import Flask, request, Response
from flask_cors import CORS
from flask_htpasswd import HtPasswdAuth

from api.helpers.auth import Auth
from api.helpers.password import Password
from api.helpers.utils import Utils
from api.helpers.config import Config

# app = Flask(__name__)
app = Flask(__name__)
app.config['FLASK_HTPASSWD_PATH'] = f'{str(Path.home())}/.m2ag-labs/.htpasswd'
app.config['FLASK_SECRET'] = '8675309'
CORS(app)
htpasswd = HtPasswdAuth(app)


# jwt to access this thing with
@app.route('/auth', methods=['GET'])
@htpasswd.required
def get_token(user):
    if request.method == 'GET':
        return format_return(Auth.get_token())


# manage config files -- 4.27
# get the whole thing -- limit to get for now since config is assembled
@app.route('/config', methods=['GET'])
@htpasswd.required
def get_config(user):
    if request.method == 'GET':
        return format_return(Config.get_config())


@app.route('/config/features', methods=['GET'])
@htpasswd.required
def get_config_features(user):
    if request.method == 'GET':
        return format_return(Config.get_features())


@app.route('/config/server', methods=['GET', 'PUT'])
@htpasswd.required
def get_put_server(user):
    if request.method == 'GET':
        return format_return(Config.get_server())
    elif request.method == 'PUT':
        return format_return(Config.put_server(request.get_json()))

    else:
        return 'access to that service not allowed', 204


# section = thing or component, component is the file to delete
@app.route('/config/things/<thing>', methods=['GET', 'PUT', 'DELETE'])
@htpasswd.required
def section_component(user, thing):
    if request.method == 'GET':
        return format_return(Config.get_module(thing))
    elif request.method == 'PUT':
        pass
        return format_return(Config.put_module(section, component, request.get_json()))
    elif request.method == 'DELETE':
        pass
        return format_return(Config.delete_module(section, component))


# 4.27
@app.route('/config/enabled', methods=['GET', 'PUT'])
@htpasswd.required
def get_enabled(user):
    if request.method == 'GET':
        return format_return(Config.get_enabled())
    elif request.method == 'PUT':
        return format_return(Config.put_enabled(request.get_json()))
    else:
        return 'access to that route not allowed', 204


@app.route('/things/<module>', methods=['GET', 'PUT', 'DELETE'])
@htpasswd.required
def get_put_thing(user, module):
    if request.method == 'GET':
        return format_return(Config.get_component_thing(module, True))
    elif request.method == 'PUT':
        return format_return(Config.put_component_thing(module, request.get_json(), True))
    elif request.method == 'DELETE':
        return format_return(Config.delete_component_thing(module, True))
    else:
        return 'access to that service not allowed', 204


@app.route('/components/<module>', methods=['GET', 'PUT', 'DELETE'])
@htpasswd.required
def get_put_component(user, module):
    if request.method == 'GET':
        return format_return(Config.get_component_thing(module, False))
    elif request.method == 'PUT':
        return format_return(Config.put_component_thing(module, request.get_json(), False))
    elif request.method == 'DELETE':
        return format_return(Config.delete_component_thing(module, False))
    else:
        return 'access to that service not allowed', 204


@app.route('/pip/<package>', methods=['GET', 'PUT'])
@htpasswd.required
def get_put_pip(user, package):
    if request.method == 'GET':
        if package != '--list--':
            return format_return(Utils.get_pip(package))
        else:
            return format_return(Utils.get_pip_list())

    elif request.method == 'PUT':
        return format_return(Utils.put_pip(package))

    else:
        return 'access to that service not allowed', 204


@app.route('/<service>/<action>', methods=['GET'])
@htpasswd.required
def service_action(user, service, action):
    if service in ['m2ag-thing', 'm2ag-motion', 'm2ag-homeassistant', 'm2ag-indicator', 'm2ag-gateway']:
        # the service web component prefixes everything with m2ag-
        if service == 'm2ag-motion':
            return format_return(Utils.service_action('motion', action))
        else:
            return format_return(Utils.service_action(service, action))
    else:
        return 'access to that service not allowed', 200


@app.route('/password', methods=['PUT', 'GET', 'POST', 'DELETE'])
@htpasswd.required
def password(user):
    if request.method == 'PUT':
        return format_return(Password.change_password(request.get_json()))
    if request.method == 'GET':
        return format_return(Password.get_users())
    if request.method == 'POST':
        return format_return((Password.add_user(request.get_json())))
    if request.method == 'DELETE':
        return format_return((Password.delete_user(request.get_json())))


def format_return(data):
    return Response(json.dumps({'data': data}), mimetype='application/json')


if __name__ == '__main__':
    if os.path.isfile(f'{str(Path.home())}/.m2ag-labs/ssl/server.crt') and os.path.isfile(
            f'{str(Path.home())}/.m2ag-labs/ssl/server.key'):
        context = (f'{str(Path.home())}/.m2ag-labs/ssl/server.crt', f'{str(Path.home())}/.m2ag-labs/ssl/server.key')
        app.run(host='0.0.0.0', port='5000', ssl_context=context)
    #  app.run(host=f'{socket.gethostname()}.local', port='5000', ssl_context=context)
    else:
        app.run(host='0.0.0.0', port='5000')
