from tornado import ioloop
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
        self.main_loop = ioloop.IOLoop.current()
        # are there any buttons in the component:
        if hasattr(self.component, 'attr'):
            for i in component.attr:
                getattr(self.component, i).when_pressed = lambda: self.main_loop.add_callback(lambda: self.set_property(i, True))
                if component.attr[i]['release']:
                    getattr(self.component, i).when_released = lambda: self.main_loop.add_callback(lambda: self.set_property(i, False))

        if 'poll' in conf:
            self.poll = conf['poll']
            logging.debug(self.title + ' starting the sensor update looping task')
            self.timer = ioloop.PeriodicCallback(
                self.poll_component,
                self.poll['poll_interval']
            )
            self.timer.start()

    def poll_component(self):
        for key in self.poll['members']:
            # noinspection PyBroadException
            try:
                t = self.component.get(key)
                o = getattr(self, key)
                o.notify_of_external_update(t)
            except:
                self.logging.error(key, ' not found in poll')

    def cancel_update_task(self):
        self.timer.stop()

