from setuptools import find_packages, setup

requirements = []
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="searchlib",
    packages=find_packages(include=["searchlib"]),
    version="0.1.0",
    description="A library to match and compare strings.",
    author="atomflunder",
    license="MIT",
    requires=requirements,
    tests_require=["pytest"],
    test_suite="tests",
)
