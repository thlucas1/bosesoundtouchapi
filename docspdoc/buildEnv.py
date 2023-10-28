# add project drectory to python search paths for relative references
import sys
sys.path.append(".")

import os

# our package constants.
from bosesoundtouchapi.bstconst import (
    PACKAGENAME,
    VERSION,
    PDOC_BRAND_ICON_URL,
    PDOC_BRAND_ICON_URL_SRC,
    PDOC_BRAND_ICON_URL_TITLE
)

# this script simply prints "VARIABLE=VALUE" lines that will be used to
# set DOS environment variables via the following command:
#   FOR /F %G IN ('"python .\docspdoc\buildEnv.py"') DO SET '%G'

if __name__ == "__main__":

    # current package name:
    print("BUILDENV_PACKAGENAME={0}".format(PACKAGENAME))

    # current package version:
    print("BUILDENV_PACKAGEVERSION={0}".format(VERSION))

    # PDoc documentation variables:
    print("BUILDENV_PDOC_BRAND_ICON_URL={0}".format(PDOC_BRAND_ICON_URL))
    print("BUILDENV_PDOC_BRAND_ICON_URL_SRC={0}".format(PDOC_BRAND_ICON_URL_SRC))
    print("BUILDENV_PDOC_BRAND_ICON_URL_TITLE={0}".format(PDOC_BRAND_ICON_URL_TITLE))
