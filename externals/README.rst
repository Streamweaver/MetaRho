Dependencies and Externals
==========================

Various external libraries are used with this application.  Information and some
helpful information about how to use them as well.

Django Pagination
-----------------

The `Django Pagination <http://code.google.com/p/django-pagination/>`_ external
is a popular template pagination tool.

From the *externals/* directory check out http://django-pagination.googlecode.com/svn/trunk/pagination
to pagination/ with a command like::

    svn checkout http://django-pagination.googlecode.com/svn/trunk/pagination pagination/

Mime Parse
----------

`Mimeparse <http://code.google.com/p/mimeparse/source/browse/trunk/mimeparse.py>`_
is a great set of scripts and modules in a number of different languages for
robust parsing of mimetypes.

It is used here for content negotiation.

Either install `mimeparse.py <http://code.google.com/p/mimeparse/source/browse/trunk/mimeparse.py>`_
or to go *externals/* and do an svn checkout on::

    svn checkout http://mimeparse.googlecode.com/svn/trunk/mimeparse.py