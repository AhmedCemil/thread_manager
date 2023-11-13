from setuptools import setup

setup(
    name="thread_manager",
    version="0.1",
    packages=['thread_manager'],
    url='https://github.com/AhmedCemil/thread_manager',
    license='MIT',
    author="Ahmed Cemil Bilgin",
    author_email="ahmed.c.bilgin@gmail.com",
    description="Thread Manager Library",
    install_requires=[
        'infi.systray',
        'notify-py',
        'pycaw',
    ],
)
