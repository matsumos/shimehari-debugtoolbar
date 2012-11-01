import os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

try:
    README = open(os.path.join(here, 'README.rst')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()
except:
    README = ''
    CHANGES = ''


setup(
    name='Shimehari-DebugToolbar',
    version='0.1.1',
    url='http://github.com/matsumos/shimehari-debugtoolbar',
    license='BSD',
    author='Keiichiro Matsumoto',
    author_email='matsumos@gmail.com',
    maintainer='Keiichiro Matsumoto',
    maintainer_email='matsumos@gmail.com',
    description='A port of the Django debug toolbar to Shimehari',
    long_description=README + '\n\n' + CHANGES,
    zip_safe=False,
    platforms='any',
    include_package_data=True,
    packages=['shimehari_debugtoolbar',
              'shimehari_debugtoolbar.panels',
              'shimehari_debugtoolbar.helpers'
    ],
    install_requires=[
        'Shimehari>=0.1.10',
        'Blinker',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
