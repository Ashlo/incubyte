from setuptools import setup, find_packages

setup(
    name="hospital_vaccination",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'pandas>=2.0.0',
        'sqlalchemy>=1.4.46',
        'pytest>=7.3.1',
    ],
) 