"""
Setup file for Personal Productivity Agentic System
"""
from setuptools import setup, find_packages

setup(
    name="productivity-agent-system",
    version="1.0.0",
    description="Personal Productivity Agentic System using CrewAI",
    author="Your Name",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        'crewai>=1.0.0',
        'crewai-tools>=0.1.0',
        'langchain>=0.1.0',
        'langchain-openai>=0.0.2',
        'langchain-community>=0.0.10',
        'python-dotenv>=1.0.0',
        'pandas>=2.0.0',
        'numpy>=1.24.0',
        'requests>=2.31.0',
        'pydantic>=2.0.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'streamlit>=1.29.0',
            'plotly>=5.18.0',
        ]
    }
)