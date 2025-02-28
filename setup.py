import os
from setuptools import setup, find_packages

# our package constants.
from bosesoundtouchapi.bstconst import (
    VERSION
)

# setup constants.
NAME = 'bosesoundtouchapi'
DESCRIPTION = 'BOSE SoundTouch API Python3 Library'

# if installing using less than Python v3, then stop the install!
import sys
if sys.version_info < (3,4):
    sys.exit('Sorry, Python < 3.4 is not supported.')

# function to read the contents of the README.md file, and return it to the caller.
def readme(pathName:str):
    with open(pathName) as f:
        return f.read()

# function to build a list of files in a directory.
def getDirFilesList(pathName:str) -> list[str]:
    print(str.format("getting list of files in path \"{0}\" ...", pathName))
    dir_list = os.listdir(pathName)
    files:list[str] = []
    for file in dir_list:                       # process all matches.
        if os.path.isfile(pathName + file):     # only include files (not directories)
            files.append(str(pathName + file))
    return files

# package setup.
setup(
    # basic package information.
    name=NAME,
    version=VERSION,
    author='Todd Lucas',
    author_email='<thlucas@yahoo.com>',
    description=DESCRIPTION,
    
    # use the README.md markdown file for the description.
    long_description_content_type='text/markdown',
    long_description=readme('README.md'),
    
    # find and include all packages in the project (anything with an '__init__.py' file).
    packages=find_packages(),
    
    # place documentation folder named "docs" in the package folder.
    data_files=[
        ('../../bosesoundtouchapi/docs', getDirFilesList('docspdoc/build/')),
        ('../../bosesoundtouchapi/docs/bosesoundtouchapi', getDirFilesList('docspdoc/build/bosesoundtouchapi/')),
    ],
    
    # set minimum python version requirement.
    python_requires='>3.11.0',
    
    # set minimum dependencies requirements.
    install_requires=[
        'platformdirs>=4.1.0',
        'requests>=2.31.0',
        'smartinspectPython>=3.0.34',
        'tinytag==1.10.0',
        'urllib3>=1.21.1,<1.27',
        'websocket-client==1.6.4',
        'zeroconf>=0.132.2'
    ],
    
    # set keywords to associate this package with on Pypi.org.
    keywords=['bose', 'soundtouch', 'api', 'audio', 'speaker'],
    
    # set classifiers to associate this package with on Pypi.org.
    classifiers=[
        'Development Status :: 5 - Production/Stable',
#       'Development Status :: 2 - Pre-Alpha',
#       'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Unix',
        'Topic :: Software Development :: Libraries',
        'Topic :: Multimedia :: Sound/Audio',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License'
    ],
    
    # provide some links to list on the Pypi.org site.
    project_urls={
        'Changelog': 'https://github.com/thlucas1/bosesoundtouchapi/blob/master/CHANGELOG.md',
        'Documentation': 'https://bosesoundtouchapi.readthedocs.io/en/latest/__init__.html',
        'GitHub': 'https://github.com/thlucas1/bosesoundtouchapi',
    }
)