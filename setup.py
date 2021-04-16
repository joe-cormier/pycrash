import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycrash",
    version="0.0.17",
    author="Joe Cormier",
    author_email="joemcormier@outlook.com",
    description="software tool for simulating vehicle motion and impacts based on \
    fundamental physics and accident reconstruction techniques",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joe-cormier/pycrash",
    packages=setuptools.find_packages(exclude=("__pycache__", )),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
