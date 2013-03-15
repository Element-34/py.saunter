from setuptools import setup

setup(
    name="py.saunter",
    packages=['saunter',
              'saunter.generators',
              'saunter.po',
              'saunter.po.remotecontrol',
              'saunter.po.webdriver',
              'saunter.providers',
              'saunter.testcase'],
    package_data={"saunter": ["_defaults/conftest.py",
                              "_defaults/pytest.ini",
                              "_defaults/conf/saunter.ini.default",
                              "_defaults/tailored/remotecontrol.py",
                              "_defaults/tailored/page.py",
                              "_defaults/tailored/webdriver.py"]},
    version = "0.59",
    author = "adam goucher",
    author_email = "adam@element34.ca",
    install_requires = ['pytest>=2.3.4',
                        'pytest-marks>=0.3',
                        'pytest-xdist',
                        'requests',
                        'selenium>=2.31.0',
                        'browsermob-proxy>=0.4.0',
                        'harpy>=0.2.0'],
    license="LICENSE.txt",
    description="An opinionated Selenium framework",
    long_description="An opinionated test framework",
    url='https://github.com/Element-34/py.saunter',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Quality Assurance',
        'Programming Language :: Python'
    ],
    entry_points = {
        "console_scripts": [
            "pysaunter = saunter.main",
        ],
    }
    
)
