from setuptools import setup, find_packages
from pathlib import Path

# 读取README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="mystical-prediction",
    version="1.0.0",
    author="CJyylaiziyou",
    author_email="your_email@example.com",
    description="Advanced multi-dimensional divination system integrating 7 traditional wisdom systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CJyylaiziyou/mystical-prediction",
    project_urls={
        "Bug Tracker": "https://github.com/CJyylaiziyou/mystical-prediction/issues",
        "Documentation": "https://github.com/CJyylaiziyou/mystical-prediction/wiki",
        "Source Code": "https://github.com/CJyylaiziyou/mystical-prediction",
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
        "Intended Audience :: Developers",
        "Natural Language :: Chinese (Simplified)",
        "Natural Language :: English",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.23.4",
        "pandas>=1.5.3",
        "fastapi>=0.95.1",
        "pydantic>=1.10.7",
        "pyephem>=4.1.3",
    ],
    extras_require={
        "dev": [
            "pytest>=7.2.2",
            "pytest-cov>=4.0.0",
            "black>=23.1.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "docs": [
            "sphinx>=6.1.3",
            "sphinx-rtd-theme>=1.2.0",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="divination fortune-telling bazi ziwei tarot iching astrology",
)
