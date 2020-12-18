import json
import os
import socket


class ConfigHelper:
    @staticmethod
    def get_features():
        features = []
        if os.path.isfile("/etc/systemd/system/m2ag-thing.service"):
            features.append('m2ag-thing')
        if os.path.isfile("/etc/systemd/system/m2ag-gateway.service"):
            features.append('m2ag-gateway')
        if os.path.isfile("/etc/systemd/system/motion.service"):
            features.append('m2ag-motion')
        # TODO: look from motion in the install path
        return features

    @staticmethod
    def get_config():
        # TODO: add error check here
        # get server record -
        # do feature detection. Is motion/mozilla gateway etc installed?
        config = ConfigHelper.get_server()
        config['hardware'] = ConfigHelper.get_modules('components')
        config['things'] = ConfigHelper.get_modules('things')
        with open('./config/component_map.json', 'r') as file:
            try:
                component_map = file.read().replace('\n', "")
                component_map = json.loads(component_map)
                config['component_map'] = component_map['component_map']
            except UnicodeDecodeError:
                config['component_map'] = {}

        # add features covered in separate call.
        # config['features'] = ConfigHelper.get_features()
        return config

    @staticmethod
    def get_modules(t_dir):
        modules = {}
        entries = os.scandir('./config/available/' + t_dir + '/')
        for entry in entries:
            with open(entry.path, 'r') as file:
                try:
                    config = file.read().replace('\n', "")
                    if config != '':
                        modules[entry.name[:entry.name.find('.json')]] = json.loads(config)
                except UnicodeDecodeError: # .DStore on mac make this choke otherwise
                    pass
        return modules

    @staticmethod
    def get_module(section, component):
        with open('./config/available/' + section + '/' + component + '.json', 'r') as file:
            config = file.read().replace('\n', "")
        return json.loads(config)

    @staticmethod
    def delete_module(section, component):
        os.remove('./config/available/' + section + '/' + component + '.json')
        return os.path.exists('./config/available/' + section + '/' + component + '.json')


    @staticmethod
    def put_module(section, component, data):
        with open('./config/available/' + section + '/' + component + '.json', 'w') as file:
            if isinstance(data, dict):
                if section == 'things':
                    data['init']['title'] = data['init']['title'].replace('--HOSTNAME--', socket.gethostname())
                file.write(json.dumps(data))
            else:
                file.write(data)
        file.close()
        return ConfigHelper.get_module(section, component)

    @staticmethod
    def get_component_thing(component, thing):
        if thing:
            with open('./device/things/components/' + component + '.py', 'r') as file:
                config = file.read().replace('\n', "")
        else:
            with open('./device/hardware/components/' + component + '.py', 'r') as file:
                config = file.read().replace('\n', "")
        return config

    @staticmethod
    def put_component_thing(component, data, thing):
        if thing:
            with open('./device/things/components/' + component + '.py', 'w') as file:
                file.write(data)
        else:
            with open('./device/hardware/components/' + component + '.py', 'w') as file:
                file.write(data)
        file.close()
        return ConfigHelper.get_component_thing(component, thing)

    @staticmethod
    def delete_component_thing(component, thing):
        if thing:
            try:
                os.remove('./device/things/components/' + component + '.py')
            except FileNotFoundError:
                pass
            # return os.path.exists('./device/things/components/' + component + '.py')
            return ConfigHelper.delete_module('things', component)
        else:
            try:
                os.remove('./device/hardware/components/' + component + '.py')
            except FileNotFoundError:
                pass
            return ConfigHelper.delete_module('components', component)
            # return os.path.exists('./device/hardware/components/' + component + '.py')

    @staticmethod
    def get_component_map():
        # get the current map from config.json
        with open('./config/component_map.json', 'r') as file:
            conf = file.read().replace('\n', "")
        config = json.loads(conf)
        # get lists of available components and things
        config['components'] = [x.split('.')[0] for x in os.listdir('./config/available/components/')]
        config['things'] = [x.split('.')[0] for x in os.listdir('./config/available/things/')]
        return config

    @staticmethod
    def put_component_map(component_map):
        # get the current map from config.json
        # TODO: check for overrides in config
        config = {"component_map": component_map}
        with open('./config/component_map.json', 'w') as file:
            file.write(json.dumps(config))
        file.close()
        return ConfigHelper.get_component_map()

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
                file.write(server)
            file.close()
        return ConfigHelper.get_server()
