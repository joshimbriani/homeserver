from setuptools import setup

setup(
    name="homeserver",
    version="0.1",
    py_modules=["main"],
    install_requires=[
        "Click",
        "python-crontab"
    ],
    entry_points='''
        [console_scripts]
        homeserver=main:cli
    ''',
)