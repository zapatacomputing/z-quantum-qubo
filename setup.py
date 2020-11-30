import setuptools
import os

setuptools.setup(
    name="z-quantum-qubo",
    version="0.1.0",
    author="Zapata Computing, Inc.",
    author_email="info@zapatacomputing.com",
    description="A library containing logic for manipulating QUBOs for Orquestra.",
    url="https://github.com/zapatacomputing/z-quantum-qubo",
    packages=setuptools.find_namespace_packages(include=["zquantum.*"]),
    namespace_packages=setuptools.find_namespace_packages(include=["zquantum.*"]),
    package_dir={"": "src/python"},
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
    install_requires=["z-quantum-core", "dimod==0.9.11"],
)
