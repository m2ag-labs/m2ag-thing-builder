import tornado.ioloop
from webthing import Thing


class Generic(Thing):
    """A generic class polled service access"""

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
        if hasattr(self.component, 'update'):
            self.component.update()
        #  TODO: test with servo controller
        for key in self.poll['members']:
            if isinstance(key, dict):  # allows multiple things to one component - i.e. nest
                c = list(key.keys())[0]
                t = self.component.get({c: key})
            else:  # one thing,
                t = self.component.get(key)

            o = getattr(self, key)
            o.notify_of_external_update(t)

    def cancel_update_level_task(self):
        self.timer.stop()

