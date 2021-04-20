import importlib

try:
    import board
    import busio
except(ImportError, RuntimeError, ModuleNotFoundError):
    pass


class Services:

    def __init__(self, config, logging):

        try:
            self.i2c = busio.I2C(board.SCL, board.SDA)
            self.i2c_enabled = True
        except(ValueError, NameError):
            self.i2c_enabled = False

        self.components = {}
        # Create a dict with desired modules in it
        # Check component map and create a list of devices to create
        build = list(config['component_map'].values())
        conf = config['components']
        for k in build:
            # generate a class -- multiple things can map to one service class.
            if k in self.components:
                continue
            try:
                module = importlib.import_module('device.services.components.' + k)
                class_ = getattr(module, k.capitalize())
            except ModuleNotFoundError:
                # TODO: add other hardware -- spi, etc
                module = importlib.import_module('device.services.i2cwrapper')
                class_ = getattr(module, 'I2cWrapper')

            if 'svc' in conf[k]['init'] and conf[k]['init']['svc'] == 'i2c':
                if self.i2c_enabled:
                    cl = class_(conf[k], logging, self.i2c)
                else:
                    logging.error(f'{k} requires i2c to be enabled - skipping')
                    continue
            else:
                cl = class_(conf[k], logging)

            self.components[k] = cl
