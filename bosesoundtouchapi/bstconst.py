# our package imports.
# none.

# constants are placed in this file if they are used across multiple files.
# the only exception to this is for the VERSION constant, which is placed here for convenience.

VERSION:str = "1.0.55"
""" 
Current version of the Bose SoundTouch API Python3 Library. 
"""

PACKAGENAME:str = "bosesoundtouchapi"
"""
Name of our package (used by PDoc Documentation build).
"""

# properties used in PDOC documentation build.

PDOC_BRAND_ICON_URL:str = "https://www.bose.com"
"""
PDoc Documentation brand icon link url that is displayed in the help document TOC.  
"""

PDOC_BRAND_ICON_URL_SRC:str = "bosesoundtouchapi.ico"
"""
PDoc Documentation brand icon link url that is displayed in the help document TOC.  
"""

PDOC_BRAND_ICON_URL_TITLE:str = "A SoundTouch Client"
"""
PDoc Documentation brand icon link title that is displayed in the help document TOC.  
"""

# miscellaneous constants.

UNKNOWN_VALUE:str = "<unknown>"
"""
Indicates if an event argument value is unknown for event argument objects that are displayed as a string.  
"""

BOSE_DEVELOPER_APPKEY:str = "Ml7YGAI9JWjFhU7D348e86JPXtisddBa"
"""
Bose Developer application key used for notifications.
"""

# application trace messages.

MSG_TRACE_ACTION_KEY:str = "Sending '%s' key (state=%s) action to SoundTouch device: '%s'"
"""
Sending '%s' key press and release to SoundTouch device: '%s'
"""

MSG_TRACE_BOOKMARKS_NOT_ENABLED:str = "Current NowPlaying item is not enabled for bookmarks: '%s'"
"""
Current NowPlaying item is not enabled for bookmarks: '%s'
"""

MSG_TRACE_DELAY_DEVICE:str = "Delaying for %d seconds to allow SoundTouch device '%s' to process the change"
"""
Delaying for %d seconds to allow SoundTouch device '%s' to process the change
"""

MSG_TRACE_DEVICE_COMMAND:str = "Executing command '%s' on SoundTouch device: '%s'"
"""
Executing command '%s' on SoundTouch device: '%s'
"""

MSG_TRACE_DEVICE_COMMAND_WITH_PARM:str = "Executing command '%s' (%s) on SoundTouch device: '%s'"
"""
Executing command '%s' (%s) on SoundTouch device: '%s'
"""

MSG_TRACE_FAVORITE_NOT_ENABLED:str = "Current NowPlaying item is not enabled for favorites: '%s'"
"""
Current NowPlaying item is not enabled for favorites: '%s'
"""

MSG_TRACE_GET_CONFIG_OBJECT:str = "Getting %s configuration for SoundTouch device: '%s'"
"""
Getting %s configuration for SoundTouch device: '%s'
"""

MSG_TRACE_RATING_NOT_ENABLED:str = "Current NowPlaying item is not enabled for ratings: '%s'"
"""
Current NowPlaying item is not enabled for ratings: '%s'
"""

MSG_TRACE_SET_PROPERTY_VALUE_SIMPLE:str = "Setting %s to '%s' on SoundTouch device: '%s'"
"""
Setting %s to '%s' on SoundTouch device: '%s'
"""
