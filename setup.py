from distutils.core import setup

setup(
    name='automower',
    version='0.1dev',
    packages=['automower',],
    license='LICENCE.txt',
    install_requires=[
        # 'transitions',
        "apscheduler"
        
    ]
)