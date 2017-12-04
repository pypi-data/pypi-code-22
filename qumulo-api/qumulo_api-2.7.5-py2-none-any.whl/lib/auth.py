# Copyright (c) 2012 Qumulo, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

import base64
import collections
import errno
from hashlib import sha256
import hmac
import os
import json
from random import SystemRandom
from tempfile import NamedTemporaryFile
import time

# See http://tools.ietf.org/html/draft-hammer-oauth-v2-mac-token-05

CREDENTIALS_FILENAME = ".qfsd_cred"
CONTENT_TYPE_BINARY = "application/octet-stream"
CREDENTIALS_VERSION = 1

def encode_nonce(s):
    "Use web-safe base64 encoding without padding for simple nonce string"
    return base64.urlsafe_b64encode(s).strip("=")

class Credentials(object):
    # If you change the credential structure, bump CREDENTIALS_VERSION above!
    # XXX qat: Bearer token cleanup : US946
    #           Eventually, all callers should provide only the bearer_token.
    #           issue, key, key_id, and algorithm can be removed
    #           bearer_token should just be required arguments.
    def __init__(self, issue=None, key=None, key_id=None, algorithm=None,
            bearer_token=None):
        self.issue = issue
        self.bearer_token = bearer_token

        # XXX qat: Bearer token cleanup : US946
        self.algorithm = algorithm
        self.key = str(key)
        self.key_id = str(key_id)

    @classmethod
    def from_login_response(cls, obj):
        # XXX qat: Bearer token cleanup : US946
        # bearer token should always be provided
        # issue, key, key_id, algoritm can be removed completely
        tmp_issue = obj.get('issue', None)
        tmp_issue = int(tmp_issue) if tmp_issue is not None else None
        return cls(
            issue=tmp_issue,
            bearer_token=obj.get('bearer_token', None),
            key=obj.get('key', None),
            key_id=obj.get('key_id', None),
            algorithm=obj.get('algorithm', None))

    def make_nonce(self):
        elapsed = max(0, int(time.time()) - int(self.issue))
        nonce_string = encode_nonce(str(SystemRandom().getrandbits(32)))
        return "%d:%s" % (elapsed, nonce_string)

    def make_bodyhash(self, body):
        "Body as it goes on the wire, or None if no body"
        assert body is None or isinstance(body, str)
        sha = sha256()
        if body is not None:
            sha.update(body)
        # bodyhash is standard base64 and padded
        return base64.b64encode(sha.digest())

    def sign(self, text):
        "Sign text with secret key"
        mac = hmac.new(self.key, text, sha256)
        # mac is standard base64 and padded
        return base64.b64encode(mac.digest())

    def sign_normalized_request(self, normalized):
        "Construct a text to sign from a normalized request"
        text = ""
        for value in normalized.values():
            if value is None:
                text += '\n'
            text += value.encode('utf8') + '\n'
        return self.sign(text)

    METHODS = ("GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS")
    BINARY_METHODS = ("PATCH", "PUT", "POST")
    NO_CONTENT_METHODS = ("GET", "DELETE", "HEAD", "OPTIONS", "POST")

    def auth_header(self, scheme=None, host=None, port=None, method=None,
                    uri=None, content_length=0, body=None, content_type=None):
        """
        The host and URI parameters and body will be utf8 encoded.
        The body may be None if the content length is 0 and the method is
        one of (GET, DELETE, HEAD, OPTIONS, POST).
        The URI should already have been escaped by the caller.
        """
        assert scheme in ("http", "https")
        assert host != ""
        method = method.upper()
        assert method in self.METHODS

        if content_type == CONTENT_TYPE_BINARY:
            body = None
            assert method in self.BINARY_METHODS
        else:
            if not body:
                assert content_length == 0
                body = None
            assert body or method in self.NO_CONTENT_METHODS

        if port is None:
            port = "80" if scheme == "http" else "443"
        else:
            port = str(port)

        if self.bearer_token:
            return 'Bearer {}'.format(str(self.bearer_token))
        else:
            # XXX qat: Bearer token cleanup : US946
            # when CLI is migrated this branch can be deleted and we can
            # assert that the bearer token is present
            auth = {
                'id' : self.key_id,
                'nonce' : self.make_nonce(),
                'bodyhash' : self.make_bodyhash(body),
                'mac' : None
            }

            normalized = collections.OrderedDict()
            normalized['nonce'] = auth['nonce']
            normalized['method'] = method
            normalized['uri'] = uri
            normalized['host'] = host.lower()
            normalized['port'] = port
            normalized['bodyhash'] = auth['bodyhash']
            # though ext is optional and we do not use it, it is signed as empty
            normalized['ext'] = ""
            auth['mac'] = self.sign_normalized_request(normalized)

            return 'MAC id="%(id)s", nonce="%(nonce)s", ' \
                   'bodyhash="%(bodyhash)s", mac="%(mac)s "' % auth

def credential_store_filename():
    home = os.getenv("HOME")
    path = os.path.join(home, CREDENTIALS_FILENAME)
    if os.path.isdir(path):
        raise EnvironmentError("Credentials store is a directory: %s" % path)
    return path

def remove_credentials_store(path):
    try:
        os.unlink(path)
    except EnvironmentError, e:
        if e.errno != errno.ENOENT:
            raise

def set_credentials(login_response, path):
    login_response["version"] = CREDENTIALS_VERSION
    cred_pre = os.path.basename(path) + '.'
    cred_dir = os.path.dirname(path)
    cred_tmp = NamedTemporaryFile(prefix=cred_pre, dir=cred_dir, delete=False)
    try:
        os.fchmod(cred_tmp.file.fileno(), 0600)
        cred_tmp.write(json.dumps(login_response) + '\n')
        cred_tmp.flush()
        cred_tmp.close()
        os.rename(cred_tmp.name, path)
    finally:
        if os.path.exists(cred_tmp.name):
            os.unlink(cred_tmp.name)

def get_credentials(path):
    if not os.path.isfile(path):
        return None
    store = open(path, "r")
    if os.fstat(store.fileno()).st_size == 0:
        return None
    response = json.load(store)
    store.close()

    if response.get("version") != CREDENTIALS_VERSION:
        remove_credentials_store(path)
        return None

    return Credentials.from_login_response(response)
