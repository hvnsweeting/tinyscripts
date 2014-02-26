tinyscripts
===========

Collection of all random util scripts of mine.

Who should use this?
--------------------

No one.

Install
-------

This assumes that you use ``bash``.

Tested on Ubuntu 12.04.

Run::

    bash install.sh
    source ~/.bashrc

Language
--------

Bash4.x and Python2.7 (default on Ubuntu 12.04)
Because you will not want to install ruby, or something else to run
these scripts

Conventions
-----------

Python script should start with (notice python2)::

    #!/usr/bin/env python2

This make sure it will
not run on a system which has only python3, with an error that help you quickly
detect why.

Script name should be short and somewhat meaning.

Python script end with ``.py``

bash script ends with ``.sh``

Scripts should not use any dependencies, except when you must do that.

All scripts should be executable (chmod a+x script_name)
