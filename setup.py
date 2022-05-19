# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from setuptools import setup
from io import open

setup(
    author       = "keyiflerolsun",
    author_email = "keyiflerolsun@gmail.com",

    packages     = ["SelSik"],

    name         = "SelSik",
    version      = "0.0.1",
    url          = "https://github.com/keyiflerolsun/SelSik",
    description  = '@KekikAkademi Selenium Kütüphanesi',
    keywords     = ["SelSik", 'KekikAkademi', 'keyiflerolsun'],

    long_description_content_type = "text/markdown",
    long_description              = "".join(open("README.md", encoding="utf-8").readlines()),
    include_package_data          = True,

    license     = 'GPLv3+',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3'
    ],

    python_requires  = '>=3.10',
    install_requires = [
        "setuptools",
        "wheel",
        "Kekik",
        "KekikTaban",
        "KekikSpatula",
        "asyncio",
        "aiohttp",
        "selenium",
        "webdriver_manager",
        "selenium-stealth",
        "parsel"
    ]
)