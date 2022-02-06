from setuptools import setup

setup(
    name="tuesdaybot",
    version="0.0.1",
    packages=["tuesdaybot"],
    python_requires=">=3.6,<4",
    install_requires=["requests>=2.27,<3", "discord.py>=1.7,<2"],
    entry_points={
        "console_scripts": [
            "tuesday=tuesdaybot.main:main"
        ]
    }
)
