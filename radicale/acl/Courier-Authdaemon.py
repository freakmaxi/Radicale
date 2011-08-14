# -*- coding: utf-8 -*-
#
# This file is part of Radicale Server - Calendar Server
# Copyright © 2011 Henry-Nicolas Tourneur
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Radicale.  If not, see <http://www.gnu.org/licenses/>.

"""
Courier-Authdaemon ACL.

Authentication based on the ``python-ldap`` module
(http://www.python-ldap.org/).

"""
import socket,os,sys
from radicale import acl, config, log


COURIER_SOCKET = config.get("acl", "courier-auth_socket")


def has_right(owner, user, password):
    """Check if ``user``/``password`` couple is valid."""
    if not user or (owner not in acl.PRIVATE_USERS and user != owner):
        # No user given, or owner is not private and is not user, forbidden
        return False
        
    line = sys.argv[0] . "\nlogin\n" + user + "\n" + password
    line = len(line) + "\n" + line
    try:
      s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
      s.connect(COURIER_SOCKET)
      log.LOGGER.debug("Sending to socket the request: %s" % line)
      s.send(line)
      data = s.recv(1024)
      s.close()
    except socket.error, (value,message): 
      log.LOGGER.debug("Unable to communicate with the socket (error: %s)" % message)
      return False
    log.LOGGER.debug("Got socket response: %s" % repr(data))
    if repr(data) == "FAIL":
      return False
    return True
    