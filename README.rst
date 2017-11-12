========
rr.timer
========

A class for tracking CPU time using intuitive context manager syntax. Example:

.. code-block:: python

    import time
    from rr.timer import Timer

    def busy_sleep(duration):
        start = time.time()
        while time.time() - start < duration:
            pass

    timer = Timer()
    print(timer)
    with timer.tracking():
        assert timer.active
        print(timer)
        time.sleep(1)
        print(timer)
        busy_sleep(1)
    assert not timer.active
    print(timer)


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
