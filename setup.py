from setuptools import setup, find_packages

setup(
    name="us_visa",
    version="0.0.0",
    author="Parth Ahuja",
    author_email="parthahuja006@gmail.com",
    packages=find_packages(),  # Scans all folders with __init__.py and registers them as packages, enabling clean imports across the project.
    # Note: '-e .' in requirements.txt installs the package in editable mode — code changes reflect instantly without reinstalling.
)
