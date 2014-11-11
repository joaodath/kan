# -*- coding: utf-8 -*-
from __future__ import print_function

import json
import sys

from functools import wraps
from collections import namedtuple
from contextlib import contextmanager
from abc import abstractmethod, ABCMeta


try:
    from urllib.request import urlopen, Request, quote
    from urllib.parse import urlencode
except ImportError:
    from urllib2 import urlopen, Request, quote
    from urllib import urlencode

__all__ = (
    'AbstractBaseAPIClient',
    'GoogleBookAPIClient',
    'Book',
    'main',
)

class AbstractBaseAPIClient:
    """
    AbstractBaseAPIClient that specifies the abstractmethods
    necessary to propertly be handled.
    Unlike Java's abstract methods or C++'s pure abstract methods,
    abstract methods as defined here may have an implementation.
    In addition, the ABCs define a minimal set of methods that establish
    the characteristic behavior of the type.

    Code that discriminates objects based on their ABC type can trust that
    those methods will always be present.
    """
    __metaclass__ = ABCMeta
    @abstractmethod
    def connect():
        pass
    @abstractmethod
    def reader():
        pass

class GoogleBookAPIClient:
    """
    Implements the AbstractBaseAPIClient and talks to the google books
    api for querying and finding books.

    :return self: **GoogleBookAPIClient<self>**
    """

    def __init__(self, title):
        """
        :param title: str
        """
        self.title = title

    @property
    def url(self):
        """
        Encodes urlencoded of book.

        :return string: url
        """
        base = r'https://www.googleapis.com/books/v1/volumes'
        params = urlencode({'q': r'"{title}"'.format(title=self.title)})

        return '?'.join([base, params])

    @contextmanager
    def connect(self):
        """
        Context manager for HTTP Connection state and ensures proper handling
        of network sockets, sends a GET request.

        Exception is raised at the yield statement.

        :yield request: FileIO<Socket>
        """
        try:
            headers = {'User-Agent': 'Python'}
            request = urlopen(Request(self.url, headers=headers))
            yield request
        finally:
            request.close()

    def reader(self):
        """
        Reads raw text from the connection stream.
        Ensures proper exception handling.

        :return bytes: request
        """
        with self.connect() as request:
            if request.msg != 'OK':
                raise IOError
            request_stream = request.read().decode('utf-8')
        return request_stream


class Book:
    """
    Handles HTTP request for book.
    """

    _header = ('title', 'authors', 'imageLinks', 'categories', 'description')

    def __init__(self, title, header=_header):
        """
        :param title: string
        :param header: string
        :param interface: **Implementation<AbstractBaseAPIClient>**
        """
        self.title = title
        self.header = header
        self.delegate = GoogleBookAPIClient(title)

    def __repr__(self):
        return self.title

    def json(self):
        """
        :return dict: json
        """
        raw_text = self.delegate.reader()
        return json.loads(raw_text)


def main(title):
    """
    Main function

    :TODO: Work on argument parsing
    """
    print('Hello')

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))