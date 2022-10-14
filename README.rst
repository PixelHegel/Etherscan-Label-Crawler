=============================================================================
``Etherscan Label Crawler`` - An out-of-the-box etherscan label crawler
=============================================================================
.. image:: https://api.travis-ci.com/PixelHegel/Etherscan-Label-Crawler.svg?branch=main
        :target: https://app.travis-ci.com/github/PixelHegel/Etherscan-Label-Crawler



Installation
------------

::

    pip install etherscanlabel

Usage
-----

::

    etherscanlabel crawl <labelcategory> --header=<file-path>
    etherscanlabel -h | --help

Examples
--------

::

    etherscanlabel crawl Binance --header /path/to/header.json



Contents of requirements.txt

::

    beautifulsoup4==4.11.1
    docopt==0.6.2
    notiondict==0.1.1
    pandas==1.5.0
    requests==2.28.1
    setuptools==63.0.0
    tqdm==4.64.1


Config file
-----------
You must attach your header file, you can find an example file here: https://github.com/PixelHegel/Etherscan-Label-Crawler/blob/main/header_sample.json