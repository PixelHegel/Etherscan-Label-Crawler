'''
Author: pixelhegel pixelhegel@gmail.com
Date: 2022-10-08 13:10:59
LastEditors: pixelhegel pixelhegel@gmail.com
LastEditTime: 2022-10-14 09:45:24
FilePath: /Etherscan-Label-Crawler/setup.py
Description: 

Copyright (c) 2022 by pixelhegel pixelhegel@gmail.com, All Rights Reserved. 
'''
#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from etherscanlabel import __version__


with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
'beautifulsoup4',
'docopt',
'notiondict',
'pandas',
'requests',
'setuptools',
'tqdm'
]

setup(
    name='etherscanlabel',
    version=__version__,
    description='An out-of-the-box ehterscan label crawler, you can use it to get all the labels info from etherscan.',
    long_description=readme,
    author='Pixelhegel',
    author_email='Pixelhegel@gmail.com',
    url='https://github.com/pixelhegel/Etherscan-Label-Crawler',
    packages=[
        'etherscanlabel',
    ],
    package_dir={'etherscanlabel':
                 'etherscanlabel'},
    include_package_data=True,
    package_data={'': ['label_category_list.csv']},
    install_requires=requirements,
    license='MIT License',
    zip_safe=False,
    keywords='etherscan label crawler',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'etherscanlabel=etherscanlabel.etherscanlabel:main',
        ],
    },
)