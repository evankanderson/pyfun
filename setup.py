import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyfun_events',
    version='0.2.1',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/pypa/sampleproject',
    packages=setuptools.find_packages(),
    install_requires=[
        'cloudevents >=0.2.1, <0.3',
        'Flask>=1.0.2,<2',
        'ujson>=1.35,<2',
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Unix',
    ],
)
