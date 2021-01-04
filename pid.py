import hashlib
import random
import string
import re

_sha256_re = re.compile("^[a-f0-9]{64}$")
_pid_re = re.compile("PID:([a-f0-9]{64})")


class Pid:
    def __init__(self, identity=None):
        if not identity:
            identity = _random_sha256()
        if not _sha256_re.match(str(identity)):
            raise ValueError(
                f"The provided identity: {identity} is not a valid sha256 hex"
            )

        self.__id = identity
        self.__raw_id = bytes.fromhex(self.__id)

    def sub_pid(self, name=None):
        if not name:
            name = _random_string(10)
        h = hashlib.sha256(self.__raw_id)
        h.update(str(name).encode("utf-8"))
        return Pid(h.hexdigest())

    def topic(self, topic=[]):
        if not topic:
            return f"pid/{self.__id}/self"
        path = "/".join(topic)
        return f"pid/{self.__id}/{path}"

    def __repr__(self):
        return f"PID:{self.__id}"

    def __str__(self):
        return f"PID:{self.__id}"


def try_parse_pid(value):
    """try_parse_pid returns a PID object by parsing the
    provided value as a PID literal.

    The 'PID:' prefix MUST BE present, if the value is not a valid PID
    then None is returned
    """
    m = _pid_re.search(value)
    if not m:
        return None
    return Pid(m.group(1))


def random_pid():
    return Pid(_random_sha256())

def well_known_pid(name):
    return Pid(hashlib.sha256(str(name).encode("utf-8")).hexdigest())


def _random_sha256():
    return hashlib.sha256(_random_string(10).encode("ascii")).hexdigest()


def _random_string(size=10):
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters
    result_str = "".join(random.choice(letters) for i in range(size))
    return result_str
