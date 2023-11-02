from abc import abstractmethod, ABC


class MainStyleClass(ABC):
    def __init__(self, func):
        self.func = func  # function that will be called

    @abstractmethod
    def call_function(self):
        pass

    def display_style(self):
        """here visual style for all subclasses can be defined"""
        return self.call_function()


class ContactStyle(MainStyleClass):
    """intended to serve for functions related to contacts"""

    def call_function(self):
        print(self.func())


class NotesStyle(MainStyleClass):
    """intended to serve for functions related to notes"""

    def call_function(self):
        print(self.func())


class GeneralStyle(MainStyleClass):
    """intended to serve for other functions, not related to contacts or notes"""

    def call_function(self):
        print(self.func())
