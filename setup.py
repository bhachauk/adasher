from os import path
from setuptools import setup


this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'readme.md'), encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name='adasher',
      version='0.0.1',
      long_description=long_description,
      long_description_content_type='text/markdown',
      description='Dash with analytics utilities',
      url='https://github.com/bhanuchander210/adasher.git',
      author='Bhanuchander Udhayakumar',
      author_email='bhanuchander210@gmail.com',
      license='MIT',
      packages=['adasher'],
      include_package_data=True,
      zip_safe=False,
      install_requires=required
      )
