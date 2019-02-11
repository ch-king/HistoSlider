from inspect import getmro


class HubListener:

    """
    The base class for any object that subscribes to hub messages.
    This interface defines a single method, notify, that receives
    messages
    """

    def register_to_hub(self, hub):
        raise NotImplementedError

    def unregister(self, hub):
        """ Default unregistration action. Calls hub.unsubscribe_all on self"""
        hub.unsubscribe_all(self)

    def notify(self, message):
        raise NotImplementedError("Message has no handler: %s" % message)


def _mro_count(obj):
    return len(getmro(obj))
