![alt text](https://shurjopay.com.bd/dev/images/shurjoPay.png)
### Installation

> 📝 **NOTE** Fork the repository if you want

- First clone the repository

```
git clone https://github.com/shurjopay-plugins/sp-plugin-python

```

- Create a virtual env for the plugin development

```
python -m venv venv

```

- Activate the virtual environment

```
source venv/bin/activate
```

- Install project requirements

```
pip install -r requirements.txt
```

- Deploy to pypi

```
python setup.py install
python -m build 
python -m twine upload dist/*
provide the credentials for pypi.org account
```


