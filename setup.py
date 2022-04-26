from setuptools import find_packages, setup

version = ""
with open("stringmatch/__init__.py") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"')

required_packages = []
with open("requirements.txt", "r") as f:
    required_packages = f.read().splitlines()

readme = ""
with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="stringmatch",
    author="atomflunder",
    url="https://github.com/atomflunder/stringmatch",
    license="MIT",
    description="A library to match and compare strings.",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    version=version,
    install_requires=required_packages,
    python_requires=">=3.9",
    tests_require=["pytest"],
    test_suite="tests",
)
