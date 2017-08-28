from setuptools import find_packages, setup


setup(
    name='mantis',
    packages=find_packages(),
    author='Jason Walsh',
    author_email='jason.walsh@uphs.upenn.edu',
    url='https://github.com/pennsignals/mantis',
    license='Apache',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
    ],
    install_requires=[
        'aptos',
        'curio',
        'zmq',
    ],
    entry_points={
        'console_scripts': [
            'mantis = mantis.__main__:main',
        ],
    },
    setup_requires=[
        'pytest-runner',
        'setuptools_scm',
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
    ],
    use_scm_version=True,
    python_requires='>=3.5'
)
