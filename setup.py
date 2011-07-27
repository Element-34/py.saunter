from setuptools import setup

setup(
    name="py.saunter",
    packages=['saunter', 'saunter.generators', 'saunter.po', 'saunter.providers'],
    package_data={"saunter": ["_defaults/conftest.py",
                              "_defaults/pytest.ini",
                              "_defaults/conf/saunter.ini.default"]},
    version = "0.3",
    author = "adam goucher",
    author_email = "adam@element34.ca",
    install_requires = ['pytest>2.0.2', 'pytest-marks', 'pytest-markfiltration'],
    long_description="An opionated test framework",
    url='https://github.com/adamgoucher/py.saunter',
    scripts=['bin/pysaunter.py'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Quality Assurance',
        'Programming Language :: Python'
    ]
)