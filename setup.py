from setuptools import find_packages, setup

import searchlib

required_packages = []
with open("requirements.txt", "r") as f:
    required_packages = f.read().splitlines()

readme = ""
with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="searchlib",
    author="atomflunder",
    url="https://github.com/atomflunder/searchlib",
    license="MIT",
    description="A library to match and compare strings.",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(include=["searchlib"]),
    version=searchlib.__version__,
    install_requires=required_packages,
    python_requires=">=3.9",
    tests_require=["pytest"],
    test_suite="tests",
)
