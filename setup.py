from setuptools import setup, find_packages

setup(
    name="webreconx",
    version="0.1.0",
    description="Lightweight web reconnaissance and vulnerability scanner",
    author="Mehdi",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.2",
        "dnspython>=2.4.2",
        "rich>=13.7.0",
    ],
    entry_points={"console_scripts": ["webreconx=webreconx.cli:main"]},
    python_requires=">=3.10",
    license="MIT",
)
