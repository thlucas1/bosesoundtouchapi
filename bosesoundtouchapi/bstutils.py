# external package imports.
from datetime import datetime
import sys
from xml.etree.ElementTree import Element

"""
Utility module of helper functions.
"""

def static_init(cls):
    """
    Define the decorator used to call an initializer for a class with all static methods.
    This allows static variables to be initialized one time for the class.
    """
    if getattr(cls, "static_init", None):
        cls.static_init()
    return cls


def export(fn):
    """
    Define the decorator used to modify a module's "__all__" variable.
    This avoids us having to manually modify a module's "__all__" variable when adding new classes.
    """
    mod = sys.modules[fn.__module__]
    if hasattr(mod, '__all__'):
        mod.__all__.append(fn.__name__)
    else:
        mod.__all__ = [fn.__name__]

    return fn
    

class Event:
    """
    C# like event processing in Python3.

    <details>
        <summary>View Sample Code</summary>
    ```python
    # Define the class that will be raising events:
    class MyFileWatcher:
        def __init__(self):
            self.fileChanged = Event()      # define event

        def watchFiles(self):
            source_path = "foo"
            self.fileChanged(source_path)   # fire event

    def log_file_change(source_path):       # event handler 1
        print "%r changed." % (source_path,)

    def log_file_change2(source_path):      # event handler 2
        print "%r changed!" % (source_path,)

    # Define the code that will be handling raised events.
    watcher              = MyFileWatcher()
    watcher.fileChanged += log_file_change2
    watcher.fileChanged += log_file_change
    watcher.fileChanged -= log_file_change2
    watcher.watchFiles()
    ```
    </details>
    """

    def __init__(self, *args) -> None:
        """
        Initializes a new instance of the class.
        """
        self.handlers = set()

    def fire(self, *args, **kargs):
        """
        Calls (i.e. "fires") all method handlers defined for this event.
        """
        for handler in self.handlers:
            handler(*args, **kargs)

    def getHandlerCount(self):
        """
        Returns the number of method handlers defined for this event.
        """
        return len(self.handlers)

    def handle(self, handler):
        """
        Adds a method handler for this event.
        """
        self.handlers.add(handler)
        return self

    def unhandle(self, handler):
        """
        Removes the specified method handler for this event.

        Args:
            handler (object):
                The method handler to remove.

        This method will not throw an exception.
        """
        try:
            self.handlers.remove(handler)
        except:
            pass   # ignore exceptions.
        return self

    def unhandle_all(self):
        """
        Removes all method handlers (if any) for this event.

        This method will not throw an exception.
        """
        try:
            self.handlers.clear()
        except:
            pass   # ignore exceptions.
        return self

    # alias method definitions.
    __iadd__ = handle
    __isub__ = unhandle
    __call__ = fire
    __len__  = getHandlerCount


def _xmlFind(root:Element, tag:str, default=None) -> str:
    """
    Finds the specified xml node tag in the Element object, and returns it's inner text value.
    
    Args:
        root (xml.etree.ElementTree.Element)
            The Element object to search.
        tag (str):
            The xml node tag to search for.
        default:
            A default value to assign if the xml node tag was not found.
            
    Returns:
        The text value of the specified xml node tag if found; otherwise, the default value.
    """
    if root is None:
        return default

    # if root IS the tag, then process the root.
    if root.tag == tag:
        return root.text

    # try to find the tag - if not found then return default value; otherwise return the text.
    result = root.find(tag)
    if result is None:
        return default
    return result.text


def _xmlFind(root:Element, tag:str, default=None, defaultNoText=None) -> str:
    """
    Finds the specified xml node tag in the Element object, and returns it's inner text value.
    
    Args:
        root (xml.etree.ElementTree.Element)
            The Element object to search.
        tag (str):
            The xml node tag to search for.
        default:
            A default value to assign if the xml node tag was not found.
        defaultNoText:
            A default value to assign if the xml node tag WAS found, but had no text.
            For example: "<skipEnabled />"
            
    Returns:
        The text value of the specified xml node tag if found; otherwise, the default value.
    """
    if root is None:
        return default

    # if root IS the tag, then process the root.
    if root.tag == tag:
        if root.text is None:
            return defaultNoText
        else:
            return root.text

    # try to find the tag - if not found then return default value.
    result = root.find(tag)
    if result is None:
        return default
    
    # if the tag exists, but no inner value, then return defaultNoText value.
    if result.text is None:
        return defaultNoText
    
    # otherwise return the text.
    return result.text


def _xmlFindAttr(root:Element, tag:str, name:str, default=None) -> str:
    """
    Finds the specified attribute for an xml node tag in the Element object, and returns 
    it's value.
    
    Args:
        root (xml.etree.ElementTree.Element)
            The Element object to search.
        tag (str):
            The xml node tag to search for.
        name (str):
            The xml node attribute name to search for.
        default:
            A default value to assign if the xml node tag attribute name was not found.
            
    Returns:
        The text value of the specified xml node tag attribute name if found; 
        otherwise, the default value.
    """
    if root is None:
        return default

    # if root IS the tag, then process the root.
    if root.tag == tag:
        return root.get(name, default)

    # try to find the tag - if not found then return default value; otherwise return the text.
    result = root.find(tag)
    if result is None:
        return default
    return result.get(name, default)
    