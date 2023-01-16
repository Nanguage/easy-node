from setuptools import setup, find_packages
import re


classifiers = [
    "Development Status :: 3 - Alpha",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "License :: OSI Approved :: MIT License",
    "Intended Audience :: Science/Research",
    "Intended Audience :: Developers",
]


keywords = [
    'Node editor',
    'GUI',
]


def get_version():
    with open("easynode/__init__.py") as f:
        for line in f.readlines():
            m = re.match("__version__ = '([^']+)'", line)
            if m:
                return m.group(1)
        raise IOError("Version information can not found.")


def get_long_description():
    return "See https://github.com/Nanguage/easy-node"


def get_install_requires():
    requirements = [
        "qtpy",
    ]
    return requirements


requires_test = ['pytest', 'pytest-cov', 'flake8', 'mypy']
requires_doc = []
with open("docs/requirements.txt") as f:
    for line in f:
        p = line.strip()
        if p:
            requires_doc.append(p)


setup(
    name='easy-node',
    author='Weize Xu',
    author_email='vet.xwz@gmail.com',
    version=get_version(),
    license='MIT',
    description='A general visual graph editor for Python.',
    long_description=get_long_description(),
    keywords=keywords,
    url='https://github.com/Nanguage/easy-node',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=classifiers,
    install_requires=get_install_requires(),
    extras_require={
        'test': requires_test,
        'doc': requires_doc,
        'dev': requires_test + requires_doc,
        'pyqt5': ['pyqt5'],
        'pyqt6': ['pyqt6'],
        'pyside2': ['PySide2'],
        'pyside6': ['PySide6'],
    },
    python_requires='>=3.7, <4',
)