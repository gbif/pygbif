import requests
import re
import pygbif

# import requests_cache
# from requests_cache.core import remove_expired_responses
# import os.path
# import tempfile

# CACHE_FILE = os.path.join(tempfile.gettempdir(), 'pygbif_requests_cache')
# expire = 300
# backend = "sqlite"
# requests_cache.install_cache(cache_name=CACHE_FILE, backend=backend, expire_after=expire)
# remove_expired_responses()


class NoResultException(Exception):
    pass


def gbif_search_GET(url, args, **kwargs):
    # if args['geometry'] != None:
    #   if args['geometry'].__class__ == list:
    #     b = args['geometry']
    #     args['geometry'] = geometry.box(b[0], b[1], b[2], b[3]).wkt
    out = requests.get(url, params=args, **kwargs)
    out.raise_for_status()
    stopifnot(out.headers["content-type"])
    return out.json()


def gbif_GET(url, args, **kwargs):
    out = requests.get(url, params=args, headers=make_ua(), **kwargs)
    out.raise_for_status()
    stopifnot(out.headers["content-type"])
    return out.json()


def gbif_GET_map(url, args, ctype, **kwargs):
    out = requests.get(url, params=args, headers=make_ua(), **kwargs)
    out.raise_for_status()
    stopifnot(out.headers["content-type"], ctype)
    return out


def gbif_GET_write(url, path, **kwargs):
    out = requests.get(url, headers=make_ua(), stream=True, **kwargs)
    out.raise_for_status()
    if out.status_code == 200:
        with open(path, "wb") as f:
            for chunk in out.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
    # FIXME: removing response content-type check for now, maybe add later
    # ctype = "application/octet-stream"
    # if not re.match(ctype, out.headers["content-type"]):
    #     raise NoResultException("content-type did not contain '%s'" % ctype)
    return path


def gbif_POST(url, body, **kwargs):
    head = make_ua()
    out = requests.post(url, json=body, headers=head, **kwargs)
    out.raise_for_status()
    stopifnot(out.headers["content-type"])
    return out.json()


def gbif_DELETE(url, body, **kwargs):
    head = make_ua()
    out = requests.delete(url, json=False, headers=head, **kwargs)
    out.raise_for_status()
    return out.status_code == 204


def stopifnot(x, ctype="application/json"):
    if x != ctype:
        raise NoResultException("content-type did not equal " + ctype)


def stop(x):
    raise ValueError(x)


def make_ua():
    return {
        "user-agent": "python-requests/"
        + requests.__version__
        + ",pygbif/"
        + pygbif.__version__
    }


def is_none(x):
    return x.__class__.__name__ == "NoneType"


def is_not_none(x):
    return x.__class__.__name__ != "NoneType"


gbif_baseurl = "https://api.gbif.org/v1/"

requests_argset = [
    "timeout",
    "cookies",
    "auth",
    "allow_redirects",
    "proxies",
    "verify",
    "stream",
    "cert",
]


def bn(x):
    if x:
        return x
    else:
        return None


def parse_results(x, y):
    if y.__class__.__name__ != "NoneType":
        if y.__class__ != dict:
            return x
        else:
            if "endOfRecords" in x.keys():
                return x["results"]
            else:
                return x
    else:
        return x["results"]


def check_data(x, y):
    if len2(x) == 1:
        testdata = [x]
    else:
        testdata = x

    for z in testdata:
        if z not in y:
            raise TypeError(z + " is not one of the choices")


def len2(x):
    if isinstance(x, int):
        return len([x])
    elif isinstance(x, str):
        return len([x])
    else:
        return len(x)


def stuff(**kwargs):
    return kwargs


def check_param_lens(**kwargs):
    tmp = {k: v for k, v in kwargs.items() if v is not None}
    for k, v in tmp.items():
        if len2(v) > 1:
            raise TypeError(k + " must be length 1")


def get_meta(x):
    if has_meta(x):
        return {z: x[z] for z in ["offset", "limit", "endOfRecords"]}
    else:
        return None


def has_meta(x):
    if x.__class__ != dict:
        return False
    else:
        tmp = [y in x.keys() for y in ["offset", "limit", "endOfRecords"]]
        return True in tmp


def has(str, pattern):
    w = re.search(pattern, str)
    return w is not None


def bool2str(x):
    if x is not None:
        z = str(x).lower()
        return z
    else:
        return x
