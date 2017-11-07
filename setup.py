from setuptools import setup
import codecs
import os

def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

long_desc = """
WeiboStockAnalysis
===============

.. image:: https://
    :target: https://

.. image:: https://
    :target: http://

* easy to use as most of the data returned are pandas DataFrame objects
* can be easily saved as csv, excel or json files
* can be inserted into MySQL or Mongodb

Target Users
--------------

* financial market analyst of China
* learners of financial data analysis with pandas/NumPy
* people who are interested in China financial data

Installation
--------------

    pip install WeiboStockAnalysis
    
Upgrade
---------------

    pip install WeiboStockAnalysis --upgrade
    
Quick Start
--------------

::


    
"""


setup(
    name='WeiboStockAnalysis',
    version="0.0.1",
    description='A utility for crawling historical comments of China stocks from Weibo',
#     long_description=read("README.rst"),
    long_description = long_desc,
    author='Rubin Liu',
    author_email='rubinliu@hotmail.com',
    license='BSD',
    url='http://www.liudp.cn',
    keywords='China stock data, Weibo, Scraper',
    classifiers=['Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: BSD License'],
    packages=['WeiboStockAnalysis','WeiboStockAnalysis.data'],
    package_data={'': ['*.csv']},
)