from setuptools import setup, find_packages

setup(
    name='cstats',
    version='0.2.1',
    description='cstats generates information about your file directory.',
    long_description=open('README.rst').read(),
    url='https://github.com/mijecu25/cstats',
    author='Miguel Velez',
    author_email='miguelvelez@mijecu25.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7'
    ],
    keywords=[
        'stats',
        'tool',
        'command line',
        'file system'
    ],
    packages=find_packages(),
    install_requires=[
        'docopt>=0.6.1',
    ],
    entry_points={
        'console_scripts': [
            'cst=cstats.cstats:main'
        ],
    }
)
