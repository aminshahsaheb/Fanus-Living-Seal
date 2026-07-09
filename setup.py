from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="fanus-core",
    version="1.0.0",
    description="Epistemic AI Engine — witness truth, detect flattery, build verified knowledge",
    author="Amin Shahsaheb",
    author_email="amin@fanus.ai",
    url="https://github.com/aminshahsaheb/Fanus-Living-Seal",
    packages=find_packages(),
    install_requires=[
        "groq",
        "anthropic",
        "openai",
        "python-dotenv",
        "arxiv",
        "wikipedia-api",
        "feedparser",
        "requests",
        "httpx",
        "fastapi",
        "uvicorn",
        "google-api-python-client",
    ],
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    entry_points={
        "console_scripts": [
            "fanus=fanus.main:main",
        ],
    },
)
