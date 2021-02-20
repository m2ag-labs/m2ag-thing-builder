import json

from flask import Flask, request, Response
from api.helpers.utils import Utils
from api.helpers.password import Password
from api.helpers.auth import Auth
from config.helpers.confighelper import ConfigHelper
import os.path
from pathlib import Path


app = Flask(__name__)


# jwt to access this thing with
@app.route('/auth', methods=['GET'])
def get_token():
    if request.method == 'GET':
        return format_return(Auth.get_token())


# manage config files
# get the whole thing -- limit to get for now since config is assembled
@app.route('/config', methods=['GET'])
def get_config():
    if request.method == 'GET':
        return format_return(ConfigHelper.get_config())


@app.route('/config/features', methods=['GET'])
def get_config_features():
    if request.method == 'GET':
        return format_return(ConfigHelper.get_features())


@app.route('/config/server', methods=['GET', 'PUT'])
def get_put_server():
    if request.method == 'GET':
        return format_return(ConfigHelper.get_server())
    elif request.method == 'PUT':
        return format_return(ConfigHelper.put_server(request.get_json()))

    else:
        return 'access to that service not allowed', 204


# section = thing or component, component is the file to delete
@app.route('/config/<section>/<component>', methods=['GET', 'PUT', 'DELETE'])
def section_component(section, component):
    if section in ['components', 'things']:
        if request.method == 'GET':
            return format_return(ConfigHelper.get_module(section, component))
        elif request.method == 'PUT':
            return format_return(ConfigHelper.put_module(section, component, request.get_json()))
        elif request.method == 'DELETE':
            return format_return(ConfigHelper.delete_module(section, component))
    else:
        return 'access not allowed', 204


@app.route('/config/component_map', methods=['GET', 'PUT'])
def get_component_map():
    if request.method == 'GET':
        return format_return(ConfigHelper.get_component_map())
    elif request.method == 'PUT':
        return format_return(ConfigHelper.put_component_map(request.get_json()))

    else:
        return 'access to that service not allowed', 204


@app.route('/things/<module>', methods=['GET', 'PUT', 'DELETE'])
def get_put_thing(module):
    if request.method == 'GET':
        return format_return(ConfigHelper.get_component_thing(module, True))
    elif request.method == 'PUT':
        return format_return(ConfigHelper.put_component_thing(module, request.get_json(), True))
    elif request.method == 'DELETE':
        return format_return(ConfigHelper.delete_component_thing(module, True))
    else:
        return 'access to that service not allowed', 204


@app.route('/components/<module>', methods=['GET', 'PUT', 'DELETE'])
def get_put_component(module):
    if request.method == 'GET':
        return format_return(ConfigHelper.get_component_thing(module, False))
    elif request.method == 'PUT':
        return format_return(ConfigHelper.put_component_thing(module, request.get_json(), False))
    elif request.method == 'DELETE':
        return format_return(ConfigHelper.delete_component_thing(module, False))
    else:
        return 'access to that service not allowed', 204


@app.route('/pip/<package>', methods=['GET', 'PUT'])
def get_put_pip(package):
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
def service_action(service, action):
    if service in ['m2ag-thing', 'm2ag-motion', 'm2ag-gateway']:
        # the service webcomponent prefixes everything with m2ag-
        if service == 'm2ag-motion':
            return format_return(Utils.service_action('motion', action))
        else:
            return format_return(Utils.service_action(service, action))
    else:
        return 'access to that service not allowed', 200


@app.route('/password', methods=['PUT', 'GET', 'POST', 'DELETE'])
def password():
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
    if os.path.isfile(f'{str(Path.home())}/.m2ag-labs/ssl/server.crt') \
            and os.path.isfile(f'{str(Path.home())}/.m2ag-labs/ssl/server.crt'):
        app.run(host='127.0.0.1', port='5010')
    else:
        app.run(host='0.0.0.0', port='5000')
