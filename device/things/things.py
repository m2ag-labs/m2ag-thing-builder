from __future__ import division, print_function

import importlib
from device.things.thingbuilder import ThingBuilder


class Things:

    def __init__(self, conf, logging, device):
        self.things = []
        """
            The inclusion of things is dependent on the component map
            Each thing must have a corresponding component - generic or custom
        """
        th = conf['available']  # available
        # TODO: Add checking for component_map and things -- graceful fail
        for k in conf['enabled']:
            # generate a class
            module = importlib.import_module('device.things.generic')
            class_ = getattr(module, 'Generic')
            # add the required device to the thing
            if k in device:
                cl_ = class_(th[k]['thing'], logging, device[k])
                ThingBuilder.add_props(th[k], cl_)
                # Add properties
                self.things.append(cl_)
            else:
                logging.error(f'Thing build error: {k} was not found in devices.')
