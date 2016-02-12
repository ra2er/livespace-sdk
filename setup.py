from setuptools import setup, find_packages


REQUIREMENTS = [
    'requests',
    'mock'
]

setup(
    name='livespacesdk',
    author='Sylwester Kulpa',
    author_email='sylwester.kulpa@gmail.com',
    license='MIT',
    packages=find_packages(),
    version='0.0.1',
    install_requires=REQUIREMENTS)
