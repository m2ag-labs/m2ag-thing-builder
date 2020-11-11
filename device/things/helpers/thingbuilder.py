from device.things.helpers.valuehelper import ValueHelper as Value
from webthing import (Property)


class ThingBuilder:

    @staticmethod
    def add_props(config, thing):
        """
            Each property will have a class member for it's value object. This will
            simplify the types of value object to create.
        """

        for p in config['props']:
            pr = config['props'][p]

            _set = pr['value'][1]
            _get = pr['value'][0]
            # TODO: do I need to look for numbers and ints too?
            if not isinstance(_get, bool):
                _get = thing.component.get(_get)

            if _set != 'None':
                vl = Value(_get, lambda v: thing.component.set(v), _set)
            else:
                vl = Value(_get)

            setattr(thing, pr['name'], vl)
            prop = Property(thing, pr['name'], getattr(thing, pr['name']), pr['metadata'])
            thing.add_property(prop)

    @staticmethod
    def add_events(config, thing):
        pass

    @staticmethod
    def add_action(config, thing):
        pass
