Python Template
===============

Documentation_ -- GitHub_ 

A [simple] [general-purpose] Python template 🐍🚀🎉🦕

.. code-block:: python

    import package

    # NOTE: URI params must be strings not integers

    print("this is just for testing")


When the module containing this class is loaded, ``GitHubUser.url`` is
evaluated and so the template is created once. It's often hard to notice in
Python, but object creation can consume a great deal of time and so can the
``re`` module which uritemplate relies on. Constructing the object once should
reduce the amount of time your code takes to run.

Installing
----------

::

    pip install jigar

License
-------

GPL license_


.. _Documentation: https://jigar.readthedocs.io/
.. _GitHub: https://github.com/mohsenhariri/google-drive
.. _license: https://github.com/mohsenhariri/google-drive/blob/main/LICENSE