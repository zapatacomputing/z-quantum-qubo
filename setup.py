import site
import sys
import warnings

import setuptools

# Workaound for https://github.com/pypa/pip/issues/7953
site.ENABLE_USER_SITE = "--user" in sys.argv[1:]

try:
    from subtrees.z_quantum_actions.setup_extras import extras
except ImportError:
    warnings.warn("Unable to import extras")
    extras = {}

with open("README.md", "r") as f:
    long_description = f.read()


setuptools.setup(
    name="z-quantum-qubo",
    use_scm_version=True,
    author="Zapata Computing, Inc.",
    author_email="info@zapatacomputing.com",
    description="A library containing logic for manipulating QUBOs for Orquestra.",
    url="https://github.com/zapatacomputing/z-quantum-qubo",
    packages=setuptools.find_namespace_packages(
        include=["zquantum.*"], where="src/python"
    ),
    package_dir={"": "src/python"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    setup_requires=["setuptools_scm~=6.0"],
    install_requires=[
        "z-quantum-core",
        "dimod>=0.9.11",
        "dwave-neal>=0.5.7",
        "cvxpy~=1.1.11",
    ],
    extras_require=extras,
    package_data={"src/python": ["py.typed"]},
    zip_safe=False,
)
