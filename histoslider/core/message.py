class Message:

    """
    Base class for messages that the hub handles.

    Each message represents a specific kind of event. After clients
    register to a hub, the subscribe to specific message classes, and
    will only receive those kinds of messages.

    The message class family is hierarchical, and a client subscribing
    to a message class implicitly subscribes to all of its subclasses.

    :attr sender: The object which sent the message
    :attr tag: An optional string describing the message
    """

    def __init__(self, sender, tag=None):
        """Create a new message

        :param sender: The object sending the message
        :param tag: An optional string describing the message
        """
        self.sender = sender
        self.tag = tag

    def __str__(self):
        return '%s: %s\n\t Sent from: %s' % (type(self).__name__,
                                             self.tag or '',
                                             self.sender)


class ErrorMessage(Message):

    """ Used to send general purpose error messages """
    pass


class TreeViewCurrentItemChangedMessage(Message):

    """ Indicates that the current slide has changed """

    def __init__(self, sender, item, tag=None):
        Message.__init__(self, sender, tag=tag)
        self.item = item


class SlideImportedMessage(Message):

    """ Indicates that the slide has been imported """
    pass


class SlideRemovedMessage(Message):

    """ Indicates that the slide has been removed """
    pass
