from setuptools import find_packages, setup

version = ""
with open("stringmatch/__init__.py", encoding="utf-8") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"')

required_packages = []
with open("requirements.txt", "r", encoding="utf-8") as f:
    required_packages = f.read().splitlines()

readme = ""
with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="stringmatch",
    author="atomflunder",
    author_email="80397293+atomflunder@users.noreply.github.com",
    url="https://github.com/atomflunder/stringmatch",
    license="MIT",
    description="A library to match and compare strings.",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    package_data={"stringmatch": ["py.typed"]},
    version=version,
    install_requires=required_packages,
    python_requires=">=3.9",
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    test_suite="tests",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
