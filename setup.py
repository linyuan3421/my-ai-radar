from setuptools import setup, find_packages

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="ai-radar",
    version="0.1.0",
    author="AI Radar Project",
    description="AI行业动态雷达系统",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "ai-radar=scripts.run:main",
        ],
    },
)