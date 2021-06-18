"""An observable, settable value interface."""

from webthing import Value


class ValueHelper(Value):
    """
    A property value.

    This is used for communicating between the Thing representation and the
    actual physical thing implementation.

    Notifies all observers when the underlying value changes through an
    external update (command to turn the light off) or if the underlying sensor
    reports a new value.
    """

    def __init__(self, initial_value, value_forwarder=None, options=None):
        """
        Initialize the object.

        initial_value -- the initial value
        value_forwarder -- the method that updates the actual value on the
                           thing
        index -- to allow selection of a specific channel of a multichannel
                 device
        threshold -- used to determine if a change in value was large enough to
                 warrant an update of the property value.
        """
        self.index = None
        self.threshold = None
        if options is not None and 'index' in options:
            self.index = options['index']
        if options is not None and 'threshold' in options:
            self.threshold = options['threshold']

        Value.__init__(self, initial_value, value_forwarder)

    def set(self, value):
        """
        Set a new value for this thing.

        value -- value to set
        """
        if self.value_forwarder is not None:
            if self.index is not None and self.index is not False:
                self.value_forwarder([self.index, value])
            else:
                self.value_forwarder(value)
        # TODO: make this a read back of the set value from component
        self.notify_of_external_update(value)

    def notify_of_external_update(self, value):
        """
        Notify observers of a new value.

        Check to see if the value change is greater than or equal the one specified
        by the options['threshold'] settings

        value -- new value

        """
        if value is not None and value != self.last_value:
            if self.threshold is not None:
                if abs(value - self.last_value) >= self.threshold:
                    self.last_value = value
                    self.emit('update', value)
            else:
                self.last_value = value
                self.emit('update', value)
