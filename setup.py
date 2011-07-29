from setuptools import setup

setup(
  name='Picasso',
  version='0.0.4',
  description="A simple web framework for Python.",
  url='http://adeel.github.com/picasso',
  author='Adeel Ahmad Khan',
  author_email='adeel@adeel.ru',
  packages=['picasso', 'picasso.middleware'],
  install_requires=["pump", "pump-flash", "pump-jinja", "routes"],
  license='MIT',
  classifiers=[
    'Topic :: Internet :: WWW/HTTP :: WSGI',
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License'])