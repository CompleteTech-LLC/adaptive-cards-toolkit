from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="adaptive-cards-toolkit",
    version="0.1.0",
    author="Adaptive Cards Toolkit Team",
    author_email="info@example.com",
    description="A high-level toolkit for AI agents to create, validate, and deliver adaptive cards",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/adaptive-cards-toolkit",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "adaptive-cards-py>=0.2.4",
        "requests>=2.25.0",
    ],
    extras_require={
        "openai": ["openai>=1.0.0"],
        "dev": [
            "pytest>=6.0.0",
            "black>=21.5b2",
            "isort>=5.9.1",
            "flake8>=3.9.2",
            "mypy>=0.812",
            "pytest-cov>=2.12.0",
        ],
    },
)