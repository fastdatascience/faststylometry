from distutils.core import setup

with open("README.rst", "r") as fh:
  long_description = fh.read()

setup(
  name = 'faststylometry',
  packages = ['faststylometry'],
  version = '0.5',
  license='MIT', 
  description = 'Calculates Burrows Delta',
  long_description=long_description,
  author = 'Thomas Wood',
  #author_email = 'thomas@fastdatascience.com',
  url = 'https://freelancedatascientist.net/fast-stylometry-tutorial/',
  keywords = ['stylometry', 'nlp', 'burrows delta', 'delta', 'forensic stylometry', 'natural language processing'],
  install_requires=[
          'numpy>=1.18.5',
          'pandas>=1.1.2',
          'scikit-learn>=0.23.1',
          'nltk>=3.5'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',   
    'Intended Audience :: Developers',   
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',   
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
  include_package_data=True,
)
