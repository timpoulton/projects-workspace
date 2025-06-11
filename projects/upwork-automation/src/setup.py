from setuptools import setup, find_packages

setup(
    name="upwork_automation",
    version="0.1.0",
    description="Automate Upwork tasks",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # Add your runtime dependencies here, e.g. 'requests'
    ],
    entry_points={
        "console_scripts": [
            "upwork-automation=upwork_automation.main:main",
        ],
    },
) 