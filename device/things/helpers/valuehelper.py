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

    def __init__(self, initial_value, value_forwarder=None, index=None):
        """
        Initialize the object.

        initial_value -- the initial value
        value_forwarder -- the method that updates the actual value on the
                           thing
        index -- to allow selection of a specific channel of a multichannel
                 device
        """
        Value.__init__(self, initial_value, value_forwarder)
        self.index = index

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

        self.notify_of_external_update(value)
