from setuptools import setup

setup(
    name='recommend',
    version='0.1',
    py_modules=['recommend'],
    install_requires=[
        'pytest==2.9.2',
        'Click==6.6',
        'jsonschema==2.5.1'
    ],
    entry_points='''
        [console_scripts]
        recommend=recommend:cli
    ''',
)
