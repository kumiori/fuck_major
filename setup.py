# setup.py
from setuptools import setup, find_packages

setup(
    name="fuck_major",
    version="0.1",
    author="Andrés León Baldelli",
    author_email="leon.baldelli@cnrs.fr",
    description="A scientific journal scraper package",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/yourusername/fuck_major",  # Update this to your GitHub repository
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4",
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)