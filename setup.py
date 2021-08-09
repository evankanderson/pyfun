import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='http-containerize',
    version='0.3.15',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/evankanderson/pyfun',
    license="Apache",
    packages=setuptools.find_packages(include=("framework",)),
    install_requires=[
        'cloudevents >=1.2, <2',
        'Flask>=1.0.2,<2',
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Unix',
    ],
)
