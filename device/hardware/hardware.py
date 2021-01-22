import importlib
import platform

if platform.system() == "Darwin" or platform.system() == "Windows":
    raspi = False
else:
    raspi = True
    import board
    import busio
    from busio import I2C


class Hardware:

    def __init__(self, config, logging):

        # Create library object using our Bus I2C port
        if raspi:
            self.i2c: I2C = busio.I2C(board.SCL, board.SDA)
        else:
            self.i2c = None
        self.components = {}
        # Create a dict with desired modules in it
        # Check component map and create a list of devices to create
        build = list(config['component_map'].values())
        conf = config['components']
        for k in build:
            # generate a class -- multiple things to one service class.
            if k in self.components:
                continue
            try:
                module = importlib.import_module('device.hardware.components.' + k)
                class_ = getattr(module, k.capitalize())
            except ModuleNotFoundError:
                # TODO: add other hardware -- spi, etc
                module = importlib.import_module('device.hardware.i2cwrapper')
                class_ = getattr(module, 'I2cWrapper')
            # TODO: what about buttons and stuff?
            if self.i2c is not None and 'svc' in conf[k]['init']:
                cl = class_(conf[k], logging, self.i2c)
            else:
                cl = class_(conf[k], logging)

            self.components[k] = cl
