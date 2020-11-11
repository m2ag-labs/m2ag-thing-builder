import tornado.ioloop
from webthing import Thing


class Generic(Thing):
    """A generic class for hardware access"""

    def __init__(self, conf, logging, component):
        Thing.__init__(
            self,
            conf['init']['id'],
            conf['init']['title'],
            conf['init']['type'],
            conf['init']['description']
        )
        self.component = component
        self.logging = logging
        if 'poll' in conf:
            self.poll = conf['poll']
            logging.debug(self.title + ' starting the sensor update looping task')
            self.timer = tornado.ioloop.PeriodicCallback(
                self.poll_component,
                self.poll['poll_interval']
            )
            self.timer.start()

    def poll_component(self):
        for i in self.poll['members']:
            key = list(i)[0]
            if isinstance(i[key], dict):  # allows multiple things to one component - nest
                c = list(i[key].keys())[0]
                t = self.component.get({c: key})
                compare = i[key][c]
            else:  # one thing,
                t = self.component.get(key)
                compare = i[key]

            self.check_update(t, key, compare)

    def cancel_update_level_task(self):
        self.timer.stop()

    def check_update(self, t, key, compare):
        o = getattr(self, key)
        if isinstance(o.last_value, bool) or isinstance(o.last_value, str):
            if o.last_value != t:
                self.logging.debug(self.title + ' setting new %s level: %s', key, t)
                o.notify_of_external_update(t)
        else:
            if o.last_value is None:
                o.notify_of_external_update(t)
            elif t is None:
                o.notify_of_external_update(-1)
                self.logging.error('no value for ' + key)
            else:
                try:
                    if abs(o.last_value - t) > compare:
                        self.logging.debug(self.title + ' setting new %s level: %s', key, t)
                        o.notify_of_external_update(t)
                except:
                    if isinstance(t, str):
                        self.logging.debug(self.title + ' setting new %s level: %s', key, t)
                        o.notify_of_external_update(t)
                    else:
                        self.logging.error('invalid comparison')
