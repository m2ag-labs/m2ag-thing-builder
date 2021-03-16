from __future__ import division, print_function

import importlib
from device.things.helpers.thingbuilder import ThingBuilder


class Things:

    def __init__(self, conf, logging, device):
        self.things = []
        """
            The inclusion of things is dependent on the component map
            To have a thing created it must have a key in the map.
            The key value will be the hardware component specified. The key may be False 
            for things with no component. 
        """
        c_map = conf['component_map']
        th = conf['things']
        # TODO: Add checking for component_map and things -- graceful fail
        for k in c_map:
            # generate a class
            # TODO: make this all generic
            try:
                module = importlib.import_module('device.things.components.' + k)
                class_ = getattr(module, k.title())
                # if module is not found use generic poll class
            except ModuleNotFoundError:
                module = importlib.import_module('device.things.generic')
                class_ = getattr(module, 'Generic')

            # add the required device to the thing
            if c_map[k] in device:
                cl_ = class_(th[k], logging, device[c_map[k]])
                ThingBuilder.add_props(th[k], cl_)
                # Add properties
                self.things.append(cl_)
            else:
                logging.error(f'Thing build error: {c_map[k]} was not found in devices.')
