# -*- coding: utf-8 -*-


# Copyright (c) 2016, 2017  Red Hat, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Written by Petr Šabata <contyk@redhat.com>

supported_content = ( "rpms", )

class ModuleArtifacts(object):
    """Class representing a particular module artifacts."""

    def __init__(self):
        """Creates a new ModuleArtifacts instance."""
        self.rpms = set()

    def __repr__(self):
        return ("<ModuleArtifacts: "
                "rpms: {0}>").format(
                        repr(sorted(self.rpms))
                        )

    def __bool__(self):
        return True if self.rpms else False

    __nonzero__ = __bool__

    @property
    def rpms(self):
        """A set of NEVRAs listing this module's RPM artifacts."""
        return self._rpms

    @rpms.setter
    def rpms(self, ss):
        if not isinstance(ss, set):
            raise TypeError("artifacts.rpms: data type not supported")
        for v in ss:
            if not isinstance(v, str):
                raise TypeError("artifacts.rpms: data type not supported")
        self._rpms = ss

    def add_rpm(self, s):
        """Adds an NEVRA to the artifact set.

        :param str s: RPM NEVRA
        """
        if not isinstance(s, str):
            raise TypeError("artifacts.add_rpm: data type not supported")
        self._rpms.add(s)

    def del_rpm(self, s):
        """Removes the supplied NEVRA from the artifact set.

        :param str s: RPM NEVRA
        """
        if not isinstance(s, str):
            raise TypeError("artifacts.del_rpm: data type not supported")
        self._rpms.discard(s)

    def clear_rpms(self):
        """Clear the RPM artifacts set."""
        self._rpms.clear()
