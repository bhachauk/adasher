from os import path
from setuptools import setup, find_packages


this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'readme.md'), encoding='utf-8') as f:
    long_description = f.read()

with open('adasher_requirements.txt') as f:
    required = f.read().splitlines()

setup(name='adasher',
      version='0.0.3',
      long_description=long_description,
      long_description_content_type='text/markdown',
      description='Dash with analytics utilities',
      url='https://github.com/bhanuchander210/adasher.git',
      author='Bhanuchander Udhayakumar',
      author_email='bhanuchander210@gmail.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=required
      )
