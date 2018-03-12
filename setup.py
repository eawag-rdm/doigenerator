# _*_ coding: utf-8 _*_

from setuptools import setup, find_packages
setup(
    name = 'doigenerator',
    version = '0.1',
    packages = find_packages(),
    install_requires = ['base32_crockford>=0.3.0',
                        'docopt>=0.6.2'],
    author = 'Harald von Waldow',
    author_email = 'harald.vonwaldow@eawag.ch',
    description = ("Generates a DOI based on Crockford's base32"
                   " (http://www.crockford.com/wrmg/base32.html)."
                   " The DOI will have six characters, including one"
                   " checksum character."),
    license = " GNU AFFERO GENERAL PUBLIC LICENSE",
    keywords = 'DOI base32 Crockford',
    entry_points = {
        'console_scripts':
        ['doigenerator=doigenerator.doigenerator:main']
    }
)
