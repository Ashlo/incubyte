from setuptools import setup, find_packages

setup(
    name="hospital-vaccination",
    version="0.1",
    packages=find_packages(),
    package_data={
        'src.database': ['*.sql'],  # Include SQL files
    },
    install_requires=[
        'pandas>=2.0.0',
        'sqlalchemy>=1.4.46',
        'pytest>=7.3.1',
        'numpy>=1.21.0',
        'tabulate>=0.9.0'
    ],
) 