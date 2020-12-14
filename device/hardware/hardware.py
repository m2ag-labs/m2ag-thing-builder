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
        conf = config['hardware']
        for k in build:
            # generate a class -- multiple things to one service class.
            if k in self.components:
                continue
            module = importlib.import_module('device.hardware.components.' + k)
            class_ = getattr(module, k.capitalize())
            # TODO: what about buttons and stuff?
            if self.i2c is not None and 'svc' in conf[k]['init']:
                cl = class_(self.i2c, conf[k]['init']['config'], logging)
            elif 'config' in conf[k]['init']:
                cl = class_(conf[k]['init']['config'], logging)
            else:
                cl = class_(logging)
            # set any attributes for startup
            if len(conf[k]['attr']) > 0:
                for a in conf[k]['attr']:
                    # if this config setting is a dict -- the attribute value is an enum in module
                    if isinstance(conf[k]['attr'][a], dict):
                        t = conf[k]['attr'][a]
                        for s in t:
                            # this next line is crazy
                            setattr(getattr(cl, k), a, getattr(getattr(module, s), t[s]))
                            # we are getting the value of the enum from our module
                    else:
                        # target object, target attribute, value to set
                        # this is kind of like init -- set values at start
                        setattr(cl, a, conf[k]['attr'][a])

            self.components[k] = cl

