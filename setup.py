from setuptools import setup, find_packages

setup(
    name="redcalibur",
    version="1.0.0",
    author="PraneeshRV",
    description="AI-powered red teaming toolkit for penetration testing",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/PraneeshRV/RedCalibur",
    packages=find_packages(),
    install_requires=[
        "shodan",
        "bs4",
        "requests",
        "whois",
        "torch",
        "scikit-learn",
        "transformers"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "redcalibur-osint=redcalibur.osint.__main__:main",
        ]
    },
)
