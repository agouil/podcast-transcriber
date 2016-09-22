from distutils.core import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name='podcast_transcriber',
      version='0.1',
      description='A simple podcast transcriber',
      author='agouil',
      author_email='andreas.williams12@gmai.com',
      url='https://github.com/agouil/podcast-transcriber',
      packages=['podcast_transcriber'],
      install_requires=required)
