from setuptools import setup, find_packages

setup(
    name = 'MongoOpCat',
    version = '0.0.1',
    keywords = ('mongodb', 'oplog'),
    description = 'a simple service which can monitor mongodb oplog',
    license = 'MIT License',
    install_requires = ['pymongo>=3.1'],
    author = 'skyleft',
    author_email = 'im@andy-cheung.me',
    packages = find_packages(),
    platforms = 'any',
)