from setuptools import setup, find_packages

setup(
    name='stats',
    version='0.1.2',
    description='Stats generates information about your file directory.',
    long_description=open('README.rst').read(),
    url='https://github.com/mijecu25/stats',
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
        'command line'
    ],
    packages=find_packages(),
    install_requires=[
        'docopt>=0.6.1',
    ],
    entry_points={
        'console_scripts': [
            'stats=stats.stats:main'
        ],
    }
)
