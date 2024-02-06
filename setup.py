# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from setuptools import setup
from io         import open

setup(
    # ? Genel Bilgiler
    name         = "SelSik",
    version      = "0.3.3",
    url          = "https://github.com/keyiflerolsun/SelSik",
    description  = "@KekikAkademi Selenium Kütüphanesi",
    keywords     = ["SelSik", "KekikAkademi", "keyiflerolsun"],

    author       = "keyiflerolsun",
    author_email = "keyiflerolsun@gmail.com",

    license      = "GPLv3+",
    classifiers  = [
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3"
    ],

    # ? Paket Bilgileri
    packages         = ["SelSik"],
    python_requires  = ">=3.10",
    install_requires = [
        "setuptools",
        "wheel",
        "selenium",
        "webdriver_manager",
        "selenium-stealth",
        "parsel",
        "cssselect"
    ],

    # ? PyPI Bilgileri
    long_description_content_type = "text/markdown",
    long_description              = "".join(open("README.md", encoding="utf-8").readlines()),
    include_package_data          = True
)