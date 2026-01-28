from setuptools import find_packages, setup

setup(
    name="DatabaseManager",
    version="0.2.3",
    packages=find_packages(),
    install_requires=[
        "mysql-connector-python"
    ],
    description="MySQL Database Manager for Wind Generator Stats",
    author="Sem Hoogstad, Mike Verkaik, Hannah Saunders, Berkin Demirel",
    python_requires=">=3.8",
)
