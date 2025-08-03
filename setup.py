#!/usr/bin/env python3
"""
Setup script for Football Twitter Bot
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="football-twitter-bot",
    version="1.0.0",
    author="CrediBall",
    description="A sophisticated Twitter bot that monitors football journalists and reposts content with reliability scoring",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/football-twitter-bot",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "aiohttp>=3.9.0",
        "groq>=0.4.0",
        "playwright>=1.40.0",
        "trafilatura>=1.6.0",
        "twscrape>=0.11.0",
    ],
    entry_points={
        "console_scripts": [
            "football-bot=main:main",
        ],
    },
)