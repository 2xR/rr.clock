========
rr.timer
========

A class for tracking CPU time using intuitive context manager syntax. Example:

.. code-block:: python

    from rr.timer import Timer

    timer = Timer()
    with timer.tracking():
        assert timer.active
        foo()
        print("Time elapased after foo(): {} and {}".format(timer.cpu, timer.wall))
        bar()
    print("Time elapased after bar(): {} and {}".format(timer.cpu, timer.wall))
    assert not timer.active


Compatibility
=============

Developed and tested in Python 3.6+. The code may or may not work under earlier versions of Python 3 (perhaps back to 3.3).


Installation
============

From the github repo:

.. code-block:: bash

    pip install git+https://github.com/2xR/rr.timer.git


License
=======

This library is released as open source under the MIT License.

Copyright (c) 2017 Rui Rei
