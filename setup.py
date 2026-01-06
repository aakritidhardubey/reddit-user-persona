from setuptools import setup, find_packages

setup(
    name="reddit-persona-generator",
    version="1.0.0",
    description="Generate detailed user personas from Reddit profiles using AI",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "Flask>=2.3.0",
        "Flask-CORS>=4.0.0", 
        "openai>=1.0.0",
        "praw>=7.0.0",
        "python-dotenv>=1.0.0",
        "requests>=2.28.0"
    ],
)