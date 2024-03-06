import requests_cache
import os.path
import tempfile

def caching(
    cache=False,
    name=None,
    backend="sqlite",
    expire_after=86400,
    allowable_codes=(200,),
    allowable_methods=("GET",),
):
    """
    pygbif caching management

    :param cache: [bool] if ``True`` all http requests are cached. if ``False`` (default),
        no http requests are cached.
    :param name: [str] the cache name. when backend=sqlite, this is the path for the
        sqlite file, ignored if sqlite not used. if not set, the file is put in your
        temporary directory, and therefore is cleaned up/deleted after closing your
        python session
    :param backend: [str] the backend, one of:

     - ``sqlite`` sqlite database (default)
     - ``memory`` not persistent, stores all data in Python dict in memory
     - ``mongodb`` (experimental) MongoDB database (pymongo < 3.0 required and configured)
     - ``redis`` stores all data on a redis data store (redis required and configured)

    :param expire_after: [str] timedelta or number of seconds after cache will be expired
        or None (default) to ignore expiration. default: 86400 seconds (24 hrs)
    :param allowable_codes: [tuple] limit caching only for response with this codes
        (default: 200)
    :param allowable_methods: [tuple] cache only requests of this methods
        (default: ‘GET’)
    
    :return: sets options to be used by pygbif, returns the options you selected
        in a hash

    Note: setting cache=False will turn off caching, but the backend data still
    persists. thus, you can turn caching back on without losing your cache.
    this also means if you want to delete your cache you have to do it yourself.

    Note: on loading pygbif, we clean up expired responses

    Usage::

        import pygbif
        
        # caching is off by default
        from pygbif import occurrences
        %time z=occurrences.search(taxonKey = 3329049)
        %time w=occurrences.search(taxonKey = 3329049)

        # turn caching on
        pygbif.caching(True)
    
        %time z=occurrences.search(taxonKey = 3329049)
        %time w=occurrences.search(taxonKey = 3329049)

        # set a different backend
        pygbif.caching(cache=True, backend="redis")
        %time z=occurrences.search(taxonKey = 3329049)
        %time w=occurrences.search(taxonKey = 3329049)

        # set a different backend
        pygbif.caching(cache=True, backend="mongodb")
        %time z=occurrences.search(taxonKey = 3329049)
        %time w=occurrences.search(taxonKey = 3329049)
        
        # set path to a sqlite file
        pygbif.caching(name = "some/path/my_file")
    """
    default_name = "pygbif_requests_cache"
    if not cache:
        requests_cache.uninstall_cache()
        CACHE_NAME = None
    else:
        if name is None and backend == "sqlite":
            CACHE_NAME = os.path.join(tempfile.gettempdir(), default_name)
        else:
            CACHE_NAME = default_name

        requests_cache.install_cache(
            cache_name=CACHE_NAME, backend=backend, expire_after=expire_after
        )
        requests_cache.delete(expired=True)

    cache_settings = {
        "cache": cache,
        "name": CACHE_NAME,
        "backend": backend,
        "expire_after": expire_after,
        "allowable_codes": allowable_codes,
        "allowable_methods": allowable_methods,
    }
    return cache_settings
