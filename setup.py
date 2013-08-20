from setuptools import setup

setup(
    name="saunter",
    packages=['saunter',
              'saunter.generators',
              'saunter.po',
              'saunter.po.remotecontrol',
              'saunter.po.webdriver',
              'saunter.providers',
              'saunter.testcase'],
    package_data={"saunter": ["_defaults/conftest.py",
                              "_defaults/pytest.ini",
                              "_defaults/conf/saunter.yaml.default",
                              "_defaults/conf/selenium.yaml.default",
                              "_defaults/conf/browsers/browser.yaml.default",
                              "_defaults/tailored/remotecontrol.py",
                              "_defaults/tailored/page.py",
                              "_defaults/tailored/webdriver.py"]},
    version = "2.0.0a1",
    author = "adam goucher",
    author_email = "adam@element34.ca",
    install_requires = ['pytest>=2.3.5',
                        'pytest-marks>=0.3',
                        'pytest-xdist',
                        'requests',
                        'selenium>=2.35.0',
                        'browsermob-proxy>=0.5.0',
                        'harpy>=0.2.0'],
    license="LICENSE.txt",
    description="An opinionated Selenium framework",
    long_description="An opinionated test framework",
    url='https://github.com/Element-34/py.saunter',
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
    ],
    entry_points = {
        "console_scripts": [
            "saunter = saunter.main",
        ],
    }
    
)
