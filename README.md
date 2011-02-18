(Selenium) Page Objects in Python
=================================

Page Objects 101
----------------
'Page Objects' is a pattern for creating Selenium scripts that makes heavy use of OO principles to enable code reuse and improve maintenance. Rather than having test methods that are a series of Se commands that are sent to the server, your scripts become a series of interactions with objects that represent a page (or part of one) -- thus the name.  

Without Page Objects
    public function example()
    {
      self.selenium.open('/')
      self.selenium.click('css=div.account_mast a:first')
      self.selenium.waitForPageToLoad("30000")
      self.selenium.type('username', 'monkey')
      self.selenium.type('password', 'buttress')
      self.selenium.click('submit')
      self.selenium.wait_for_page_to_Load("30000")
      self.assertEqual(self.selenium.get_ext("css=div.error > p"), "Incorrect username or password.")
    }

With Page Objects
    public function example()
    {
      landing_Page = LandingPage()
      landing.open_default_base_url()
      form = landing->open_sign_in_form()
      form.username = "monkey"
      form.password = "buttress"
      form.login()
      self.assertEqual(form.error_message, "Incorrect username or password.")
    }

As you can see, not only is the script that uses POs [slightly] more human readable, but it is much more maintainable since it really does separate the page interface from the implementation so that _when_ something on the page changes only the POs themselves need to change and not ten billion scripts.

For more information on Page Objects in Python see [this article I wrote for the Pragmatic Magazine](http://www.pragprog.com/magazines/2010-08/page-objects-in-python) -- which has some bugs and I've evolved it a bit, but its the basis for everything else.

Installation
------------
In order to make the most out of Selenium and Python; and to use the example code here, you need to

sudo pip install nose
sudo pip install unittest2
sudo pip install sphinx
sudo pip install selenium

Note: On OSX, use something other than the default Python installation; it doesn't like easy_install/pip much

Script Execution
----------------

In order to run the scripts, you first need to run the Selenium server.

From there it is a matter of using the 'run' script. Because we are using 'tags' for discovery you need to specify which tag you want. For instance, this is for all the scripts tagged with 'goals'

./run.sh tags=goals

To specify more than one tag, you need to provide additional -a flags to the script (the first is implicit and baked into run.sh).

./run.sh tags=goals -a tags=issues

This will run all the scripts for 'goals' and 'issues'

Tags
----
Part of the reason for using nose as the runner is its ability to discover scripts via 'tags' through the [nose attribute plugin](http://somethingaboutorange.com/mrl/projects/nose/0.11.1/plugins/attrib.html). This is set using the attr decorator above a test method.

    @attr(tags=['foo'])
    
This helps solve the inevitable venn diagram problem of 'this is a foo script, that deals with bar, on bif'. Without tags you need to decide on a single way of identifying the but with tags you add as many as needed.

All scripts should have at least one tag, and that is what I call the depth
- 'shallow' scripts are ones that 'must pass before you know that the current commit is good'. Think of these as 'sanity' or 'smoke' scripts but I can't think of a nice opposite of either term
- 'deep' scripts are everything else and don't need to be run with as great frequency (say, once a day)

From there, the tags can be whatever you need to describe the script. For instance,

    @attr(tags=['foo', 'bar', 'bif'])
    
is a foo test for bar, specifically for bif. The actual cloud / taxonomy is a good candidate for a wiki page. Especially once more people are adding scripts.

When working on a specific script it is often useful to add a tag of 'debug' or 'dancingelephant' or something else that is not in use elsewhere in the tag cloud.

Jenkins Integration
-------------------
Integration with the Jenkins CI server (http://jenkins-ci.org/) is a snap
1. Create a new 'free-style' job
2. Configure the job as you would normally providing it the necessary SVN credentials, polling, etc.
3. as the build step you want something like

    ./run.sh tags=foo -a tags=bar

4. the junit report is in logs/latest.xml. Even though each run produces its own result, a copy is made to latest.xml. A clone of which is stored in the job-specific directory
5. I would suggest three chained jobs like:
  * unit
  * tags=deep
  * tags=shallow

Config files
------------
By default, the framework will look in support/conf for a file called selenium.ini. There should never be a file with that name checked in to make it slightly more environment-proof. Instead, create a symlink or copy a file in place and rename it.

    Adam-Gouchers-MacBook:conf adam$ ls -l
    total 16
    lrwxr-xr-x  1 adam  staff  17  4 Jan 11:18 selenium.ini -> selenium.ini.default
    -rw-r--r--@ 1 adam  staff  85  4 Jan 10:18 selenium.ini.default
    Adam-Gouchers-MacBook:conf adam$ 

This allows for individual config values as well as ones for various CI jobs. For implementation information and usage see http://element34.ca/blog/configuration-files-in-python but the gist of it is any class that inherits from CustomTestCase will have a self.cf attribute which has access to the config file information.

    self.cf.get("SauceLabs", "ondemand")

will for instance read the 'ondemand' key from the 'SauceLabs' section.

Documentation
-------------

The Page Objects are all documented using [Sphinx](http://sphinx.pocoo.org/). To generate the docs
* make sure your PYTHONPATH includes both the scripts and modules dirs as things need to be importable for parsing
* cd docs
* make html

The generated docs will be readable from docs/build/html/index.html.

Locators
--------
One of things POs help you with is isolating your locators since they are tucked away in a class rather than spread throughout your scripts. I _highly_ suggest that you go all the way and move your locators from in the actual Se calls to a dictionary in the page object module. This is one of the biggest modifications from my article where I suggested that locators should be centralized. Now, I think it is a 'smell' that your POs are not thought out properly if you think you need to have a locator in multiple POs.

    locators = {
      "username": "username",
      "password": "password",
      "submit_button": "submit",
      "error_message": "css=div.error > p"      
    }

Now your locators truly are _change in one spot and fix all the broken-ness_. DRY code is good code.

Sharing the server connection
-----------------------------
It has been pointed out to me that what I have done to share the established connection/session to the Se server is borderline evil, but I understand it which trumps evil in my books. In order to make sure we can send / receive from the Se server, I make the connection to it a Singleton which gets set set in the PO base constructor.

    def __init__(self):
        self.se = wrapper().connection

The actual scripts have no need to know about the connection.

Custom super class
------------------
If you look at the the actual script you'll notice that it extends _CustomTestCase_ and not _unittest.TestCase_ as you might expect. This little layer of redirection lets us add custom asserts and/or exceptions for readability in our scripts.

Custom synchronization would go in the _BasePage_ class as our scripts will no longer need to worry about it -- that a responsibility of the PO.

Sauce Labs OnDemand
-------------------
Running your scripts locally or in the OnDemand cloud is simply a matter of setting the various bits in the SauceLabs section of your selenium.ini file

    [SauceLabs]
    ondemand: true
    username: your_username
    key: your-key
    server_host: ondemand.saucelabs.com 
    server_port: 4444
    os: Windows 2003
    browser: *firefox
    browser_version: 3.6.

During teardown, the job name, result and tags are set in the OnDemand job information

Soft Asserts
------------
Selenium IDE has this notion of verify* which are apparently what are called 'soft asserts' as they look like an assert but don't end the script immediately. The unittest2 driver also does not have this notion but by wrapping an assert in a try/catch block you can create this behaviour. Because we have subclassed unittest.TestCase as CustomTestCase we can put the verify* commands that we need there.

    def verifyEquals(self, want, got):
      try:
          self.assertEquals(want, got)
      except AssertionError, e:
          self.verificationErrors.append(str(e))
          
Logging
-------
Logging is done through the standard [logging](http://docs.python.org/library/logging.html). Use logging intelligently in your scripts. As in, use it _very_ sparingly. I coach people to basically only use it to log things that matter and were randomly generated (like usernames, passwords, email addresses) that could assist in debugging a script failure.

Server Control
--------------
One way to make sure that the Selenium Server is on the machine _and running_ is to use Puppet or similar configuration management tools. Another way to to embed it in the repo with the rest of the script and then write a little wrapper around it. Which I have done.

    python modules/SeleniumServer.py --check
    if [ $? = 1 ]; then
      python modules/SeleniumServer.py --start
    fi
    
Exceptions
----------
Selenium will happily throw a standard exception when something times out or an incorrect locator. But since this is going to be customized for your own project, it makes sense that the project should have its own set of exceptions. Custom synchronization methods should all throw their own custom exceptions. This sample project provides a base exception for that tree.

Data Generators and Providers
-----------------------------
Hard-coded data is all sorts of evil. There are a number of ways to address this.

_random generators
If you are going to seriously automate, you need to read, and understand the Python's [random module](http://docs.python.org/library/random.html). It is used in conjunction of with the [string module](http://docs.python.org/library/string.html) to create random strings -- with the possibility of whitespace in it in the StringData 'generator'. Add and tailor to suit.

_csv provider_
Another option is to load data from an external source, like a csv file.

_django provider_
One reason to use Python as the language for automation with Selenium is if you are using Django. By being able to access the Models of the application you can source information from the Django itself.

By using this integration you can also nicely address the 'oracle problem' by validating what is seen in the browser is also in the database.

_database provider_
If you are not using Django, then you have to reach into the database itself. In this example, the database is a sqlite3 one, but the Python database API is standardized so its just a matter of switching out the initial connection
