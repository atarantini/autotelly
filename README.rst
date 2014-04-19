===========
 Autotelly
===========

Autotelly manages your Unotelly account from command-line.


Features
--------

* Register trial account
* Update your IP address
* Display information about your account


Install
-------

* Clone the repository from Github or download the package
* (optional) Create a virtual environment and switch to it::

    $ virtualenv env && source env/bin/activate

* Install dependencies::

    $ pip install -r requirements.txt


Run
---

Creating a trial account::

    $ python autotelly.py --trial

Updating your IP address::

    $ python autotelly.py --username my@username.com --password mypassword


Usage
-----

usage: autotelly.py [-h] [--trial] [--verbose] [--username USERNAME]
                    [--password PASSWORD]

Manage your Unotelly account

optional arguments:
  -h, --help           show this help message and exit
  --trial              Register an anonymous trial user to test Unotelly
                       services.
  --verbose            Show additional information about autotelly.
  --username USERNAME  Your Unotelly username. If not provided the one in
                       config.json will be used.
  --password PASSWORD  Your Unotelly password. If not provided the one in
                       config.json will be used.


Configuration
-------------

Place a `config.json` file in your autotelly path with the following format::

    {
        "username": "26crnzkr@lapibo5j.com",
        "password": "247792"
    }


Licence
-------

Released under GNU GPLv3, see COPYING file for more details.
