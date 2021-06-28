import json
import os
import socket


class Config:
    @staticmethod
    def get_features():
        features = []
        if os.path.isfile("/etc/systemd/system/m2ag-thing.service"):
            features.append('m2ag-thing')
        if os.path.isfile("/etc/systemd/system/m2ag-indicator.service"):
            features.append('m2ag-indicator')
        if os.path.isfile('/lib/systemd/system/nodered.service'):
            features.append('nodered')
        if os.path.isfile('/lib/systemd/system/pigpiod.service'):
            features.append('pigpiod')
        return features

    '''
        Used by server to read config settings
        5-14-21
    '''

    @staticmethod
    def get_server_config():
        # TODO: add error check here
        # get server record -
        # do feature detection. Is motion/mozilla gateway etc installed?
        config = Config.get_server()
        config['available'] = Config.get_modules()
        config['services'] = Config.get_features()
        with open('./config/enabled.json', 'r') as file:
            try:
                enabled = file.read().replace('\n', "")
                enabled = json.loads(enabled)
                config['enabled'] = enabled['enabled']
            except UnicodeDecodeError:
                config['enabled'] = {}

        # add features covered in separate call.
        # config['features'] = ConfigHelper.get_features()
        return config

    @staticmethod
    def get_config():
        # get_enabled returns components and things lists
        config = Config.get_enabled()
        config['server'] = Config.get_server()
        config['services'] = Config.get_features()
        return config

    @staticmethod
    def get_modules():
        # all is stored in device/available - dir for each
        modules = {}
        entries = os.scandir('./device/available/')
        for entry in entries:
            with open(entry.path, 'r') as file:
                try:
                    config = file.read().replace('\n', "")
                    if config != '':
                        modules[entry.name[:entry.name.find('.json')]] = json.loads(config)
                except UnicodeDecodeError:  # .DStore on mac make this choke otherwise
                    pass
        return modules

    @staticmethod  # -- 5-27-21
    def get_thing(thing):
        with open('./device/available/' + thing + '.json', 'r') as file:
            config = file.read().replace('\n', "")
        config = json.loads(config)
        return config

    @staticmethod
    def delete_thing(thing):
        try:
            os.remove('./device/available/' + thing + '.json')
        except FileNotFoundError:
            pass
        return os.path.exists('./device/available/' + thing + '.json')

    @staticmethod
    def put_thing(thing, data):
        with open('./device/available/' + thing + '.json', 'w') as file:
            if isinstance(data, dict):
                data['thing']['init']['title'] = data['thing']['init']['title'].replace('--HOSTNAME--',
                                                                                        socket.gethostname())
                file.write(json.dumps(data))
            else:
                file.write(data)
        file.close()
        return Config.get_thing(thing)

    @staticmethod  # 5-27-21
    def get_helper(thing):
        try:
            with open('./device/helpers/' + thing + '.py', 'r') as file:
                config = file.read()
        except FileNotFoundError:
            config = 'none'
        return config

    @staticmethod  # 5-27-21
    def put_helper(helper, request):
        with open('./device/helpers/' + helper + '.py', 'w') as file:
            file.write(request['data'])
        file.close()
        return Config.get_helper(helper)

    @staticmethod  # 5-27-21
    def delete_helper(helper):
        try:
            os.remove('./device/helpers/' + helper + '.py')
        except FileNotFoundError:
            pass
        # return os.path.exists('./device/things/' + thing + '.json')
        return Config.get_helper(helper)

    @staticmethod  # 5-27-21
    def get_enabled():
        # get the current map from config.json
        try:
            with open('./config/enabled.json', 'r') as file:
                conf = file.read().replace('\n', "")
            config = json.loads(conf)
        except UnicodeDecodeError:
            config = {'enabled': []}
        # get lists of available things and helpers
        config['available'] = [x.split('.')[0] for x in os.listdir('./device/available/')]
        config['available'].sort()
        config['helpers'] = [x.split('.')[0] for x in os.listdir('./device/helpers/')]
        config['helpers'].sort()
        return config

    @staticmethod  # 5-27-21
    def put_enabled(enabled):
        with open('./config/enabled.json', 'w') as file:
            file.write(json.dumps(enabled))
        file.close()
        return Config.get_config()

    @staticmethod
    def get_server():
        with open('./config/server.json', 'r') as file:
            server = file.read().replace('\n', "")
        server = json.loads(server)
        return server

    @staticmethod
    def put_server(server):
        # TODO: check for valid server file?
        if server is not None:
            with open('./config/server.json', 'w') as file:
                file.write(json.dumps(server))
            file.close()
        return Config.get_server()
