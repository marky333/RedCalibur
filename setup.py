from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="redcalibur",
    version="1.0.0",
    author="PraneeshRV",
    author_email="praneesh@example.com",
    description="AI-powered red teaming toolkit for penetration testing and OSINT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PraneeshRV/RedCalibur",
    project_urls={
        "Bug Tracker": "https://github.com/PraneeshRV/RedCalibur/issues",
        "Documentation": "https://github.com/PraneeshRV/RedCalibur/wiki",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "redcalibur=redcalibur.cli:main",
            "redcalibur-osint=redcalibur.osint.__main__:main",
        ]
    },
    include_package_data=True,
    package_data={
        "redcalibur": ["*.txt", "*.md"],
    },
    keywords="security, penetration-testing, osint, red-team, cybersecurity, ai",
)
