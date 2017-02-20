#!/usr/bin/python
# -*- coding: utf-8 -*-

from nose.tools import *
from unittest import SkipTest
from functools import wraps
import myanimelist.session
import myanimelist.anime
import os

import sys

class testSessionClass(object):
  @classmethod
  def setUpClass(self):
    # see if our environment has credentials.
    if 'MAL_USERNAME' and 'MAL_PASSWORD' in os.environ:
      self.username = os.environ[u'MAL_USERNAME']
      self.password = os.environ[u'MAL_PASSWORD']
    else:
      # rely on a flat textfile in project root.
      try:
        with open(u'credentials.txt', 'r') as cred_file:
          line = cred_file.read().strip().split(u'\n')[0]
        self.username, self.password = line.strip().split(u',')
      except IOError:
        self.username = self.password = None

    self.session = myanimelist.session.Session(self.username, self.password)
    self.fake_session = myanimelist.session.Session(u'no-username', 'no-password')

  def skipIfNoCredentials(inner):
    @wraps(inner)
    def wrapper(self, *args, **kwargs):
      if not self.username:
        raise SkipTest('no credentials provided for testing')
      return inner(self, *args, **kwargs)
    return wrapper

  def testFailFakeLogin(self):
    assert not self.fake_session.logged_in()
    self.fake_session.login()
    assert not self.fake_session.logged_in()
    assert not self.session.logged_in()

  def testAnime(self):
    assert isinstance(self.session.anime(1), myanimelist.anime.Anime)

  @skipIfNoCredentials
  def testLogin(self):
    assert not self.session.logged_in()
    self.session.login()
    assert self.session.logged_in()
