from setuptools import setup

desc = open('README.md').read()

setup(
  name='Picasso',
  version='0.0.2',
  description="A simple web framework for Python.",
  long_description=desc,
  url='http://adeel.github.com/picasso',
  author='Adeel Ahmad Khan',
  author_email='adeel@adeel.ru',
  packages=['picasso', 'picasso.middleware'],
  license='MIT',
  classifiers=[
    'Topic :: Internet :: WWW/HTTP :: WSGI',
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License'])