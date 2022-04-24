from setuptools import find_packages, setup

setup(
    name="searchlib",
    packages=find_packages(include=["searchlib"]),
    version="0.1.2",
    description="A library to match and compare strings.",
    author="atomflunder",
    license="MIT",
    install_requires=[
        "Levenshtein",
        "Unidecode",
    ],
    tests_require=["pytest"],
    test_suite="tests",
)
