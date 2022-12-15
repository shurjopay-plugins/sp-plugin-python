import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="shurjopay-plugin",
    version="1.0.0",
    author="Mahabubul Hasan",
    author_email="mahabubul@pranisheba.com.bd",
    maintainer="Imtiaz Rahi",
    maintainer_email="imtiaz.rahi@shurjomukhi.com.bd",
    description="Official shurjoPay python package (plugin) for merchants or service providers to connect with shurjoPay Payment Gateway v2.1",
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
