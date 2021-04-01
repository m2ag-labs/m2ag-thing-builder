import importlib


class I2cWrapper:

    def __init__(self, config, logging, i2c):
        self.logging = logging
        self.wrapped = config['init']['driver']
        self.offsets = None
        if 'offsets' in config:
            self.offsets = config['offsets']
        lib = {}
        try:
            # TODO -- what to do about multiple modules --
            lib[self.wrapped] = importlib.import_module(self.wrapped)
        except ModuleNotFoundError:
            self.logging.error(f'{self.wrapped} driver not installed')
            return
        try:
            self.device = getattr(lib[self.wrapped],
                                  config['init']['device'])(i2c, address=int(config['init']['address'], 16))
        except:  # TODO: what should the exception be?
            self.logging.error(f'{self.wrapped} did not initialize')
        # TODO: set startup attributes
        if 'attr' in config and len(config['attr']) > 0:
            for i in config['attr']:
                if type(config['attr'][i]) == dict:
                    t = config['attr'][i]
                    for s in t:
                        # get an enum from a module
                        try:
                            setattr(self.device, i, getattr(lib[s], t[s]))
                        except AttributeError:
                            logging.warning(f'{self.wrapped} attribute {i} was not set to {s} {t[s]}')
                else:
                    try:
                        setattr(self.device, i, config['attr'][i])
                    except AttributeError:
                        logging.warning(f'{self.wrapped} attribute {i} was not set to {config["attr"][i]}')

    def get(self, val):
        try:
            if self.offsets is not None and val in self.offsets:
                return getattr(self.device, val) + self.offsets[val]
            else:
                return getattr(self.device, val)
        except AttributeError:
            self.logging.error(f'{self.wrapped} {val} was not found')
            return -1

    def set(self, val):
        try:
            setattr(self.device, getattr(self.device, val[0]), val[1])
        except AttributeError:
            self.logging.error(f'{self.wrapped} could not set {val[0]} to {val[1]}')
            return -1
