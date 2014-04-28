try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'A simple python API for MP3Skull',
    'author': 'Krishna Ram Prakash R (gTux)',
    'url': 'http://github.com/geekytux/MP3SkullAPI',
    'download_url': 'http://github.com/geekytux/MP3SkullAPI',
    'author_email': 'krishnaramprakash@gmail.com',
    'version': '0.1',
    'install_requires': ['requests','json','re','bs4','urllib'],
    'packages': ['MP3SkullAPI'],
    'scripts': [],
    'name': 'mp3skull-api'
}

setup(**config)
