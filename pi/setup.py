# setup for flask app architecture

from setuptools import setup

setup(
    name='master',
    packages=['master'],
    include_package_data=True,
    install_requires=['flask',],
)
