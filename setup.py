from setuptools import setup, find_packages

setup(
    name="iroha",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "click==8.1.8",
        "Jinja2==3.1.6",
        "markdown-it-py==3.0.0",
        "MarkupSafe==3.0.2",
        "materialyoucolor==2.0.10",
        "mdurl==0.1.2",
        "nodeenv==1.9.1",
        "pillow==11.2.1",
        "Pygments==2.19.1",
        "pyright==1.1.400",
        "PyYAML==6.0.2",
        "rich==14.0.0",
        "shellingham==1.5.4",
        "typer==0.15.3",
        "typing_extensions==4.13.2",
    ],
    entry_points={
        "console_scripts": [
            "iroha=color_generator.cli:main",
        ],
    },
    python_requires=">=3.8",
)
