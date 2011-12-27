import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "django-contenteditable",
    version = "0.1",
    author = "Simone Lusenti",
    author_email = "simone@slusenti.me",
    description = ("Django support for HTML contenteditable"),
    license = "GPL",
    keywords = "django contenteditable",
    url = "https://github.com/lusentis/django-contenteditable",
    packages=['contenteditable','sample'],
    long_description="Django support for HTML contenteditable", #read('README.md'),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
)
