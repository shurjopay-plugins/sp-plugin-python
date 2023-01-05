import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="shurjopay-plugin",
    version="0.1.3",
    author="Mahabubul Hasan",
    author_email="plugindev@shurjomukhi.com.bd",
    description="Shurjopay version 2.1 payment gateway integration package for python users",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shurjopay-plugins/sp-plugin-python.git",
    project_urls={
        "Bug Tracker": "https://github.com/shurjopay-plugins/sp-plugin-python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests'],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
)
