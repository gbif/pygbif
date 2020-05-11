from geojson_rewind import rewind
from geomet import wkt
import decimal
import statistics


def wkt_rewind(x, digits=None):
    """
    reverse WKT winding order

    :param x: [str] WKT string
    :param digits: [int] number of digits after decimal to use for the return string. 
        by default, we use the mean number of digits in your string.

    :return: a string

    Usage::
        
        from pygbif import wkt_rewind
        x = 'POLYGON((144.6 13.2, 144.6 13.6, 144.9 13.6, 144.9 13.2, 144.6 13.2))'
        wkt_rewind(x)
        wkt_rewind(x, digits = 0)
        wkt_rewind(x, digits = 3)
        wkt_rewind(x, digits = 7)
    """
    z = wkt.loads(x)
    if digits is None:
        coords = z["coordinates"]
        nums = __flatten(coords)
        dec_n = [decimal.Decimal(str(w)).as_tuple().exponent for w in nums]
        digits = abs(statistics.mean(dec_n))
    else:
        if not isinstance(digits, int):
            raise TypeError("'digits' must be an int")
    wound = rewind(z)
    back_to_wkt = wkt.dumps(wound, decimals=digits)
    return back_to_wkt


# from https://stackoverflow.com/a/12472564/1091766
def __flatten(S):
    if S == []:
        return S
    if isinstance(S[0], list):
        return __flatten(S[0]) + __flatten(S[1:])
    return S[:1] + __flatten(S[1:])
