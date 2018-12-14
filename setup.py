from setuptools import setup

setup(
    name='coffeehack',
    version='1.0.0',
    description='Hacked coffee machine Skill',
    author='Yenshu',
    url='',
    download_url='',
    license='MIT',
    install_requires=['pyserial', 'configparser','netaddr', ' pycryptodome'],
    test_suite="tests",
    keywords=['snips', 'coffee'],
    packages=['coffeehack'],
    package_data={'coffeehack': ['Snipsspec']},
    include_package_data=True
)
