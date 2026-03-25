import time
import requests
import unittest

from pygbif.occurrences.download import GbifDownload, download


class DummyClass(object):
    """A dummy response as given by the requests.post, which can be used
    to mock the posting of requests"""

    text = "0003970-140910143529206"
    status_code = 201


def dummypost(*args, **kwargs):
    """function to mock the usage of the requests.post functionality"""
    return DummyClass()


class TestGbifClass(unittest.TestCase):
    def test_gbif_creation(self):
        """test the creation of the predicate class"""

        req = GbifDownload("name", "email")
        self.assertIsInstance(req.payload, dict)
        self.assertDictEqual(
            req.payload,
            {
                "creator": "name",
                "notification_address": ["email"],
                "predicate": {"predicates": [], "type": "and"},
                "sendNotification": True,
                "format": "SIMPLE_CSV",
            },
        )
        self.assertIsNone(req.request_id)

    def test_alternative_main_type(self):
        """test the addition of another predicate combiner"""
        req = GbifDownload("name", "email")
        req.main_pred_type = "or"
        self.assertIsInstance(req.payload, dict)
        self.assertDictEqual(
            req.payload,
            {
                "creator": "name",
                "notification_address": ["email"],
                "predicate": {"predicates": [], "type": "or"},
                "sendNotification": True,
                "format": "SIMPLE_CSV"
            }
        )

    # deprecated method - to be removed
    # def test_add_predicate(self):
        # """test the predicate addition"""
        # req = GbifDownload("name", "email")
        # req.add_predicate("COUNTRY", "BE", "equals")
        # self.assertIsInstance(req.payload["predicate"]["predicates"], list)
        # self.assertEqual(len(req.payload["predicate"]["predicates"]), 1)
        # self.assertIsInstance(req.payload["predicate"]["predicates"][0], dict)
        # self.assertDictEqual(
            # req.payload["predicate"]["predicates"][0],
            # {"key": "COUNTRY", "type": "equals", "value": "BE"},
        # )

    def test_add_iterative_predicate(self):
        """the the predicate addition of an iterative sequence"""
        req = GbifDownload("name", "email")
        req.add_iterative_predicate("TAXONKEY", [3189866, 2498252])
        self.assertIsInstance(req.payload["predicate"]["predicates"], list)
        self.assertEqual(len(req.payload["predicate"]["predicates"]), 1)
        self.assertIsInstance(req.payload["predicate"]["predicates"][0], dict)

        temp_pred = req.payload["predicate"]["predicates"][0]["predicates"]
        self.assertIsInstance(temp_pred, list)
        self.assertEqual(len(temp_pred), 2)
        self.assertIsInstance(temp_pred[0], dict)

        self.assertEqual(set(list(temp_pred[0].keys())), set(["key", "type", "value"]))
        self.assertEqual(req.payload["predicate"]["predicates"][0]["type"], "or")

    def test_add_geometry(self):
        """check predicate after adding a geometry"""
        req = GbifDownload("name", "email")
        req.add_geometry(
            "POLYGON((-14.06 42.55, 9.84 38.27, -7.03 26.43, -14.06 42.55))"
        )
        self.assertIsInstance(req.payload["predicate"]["predicates"], list)
        self.assertEqual(len(req.payload["predicate"]["predicates"]), 1)
        self.assertEqual(
            set(req.payload["predicate"]["predicates"][0].keys()),
            set(["type", "geometry"]),
        )

    def test_lookup_predicates(self):
        """different lookups checked"""
        # main combination predicate
        req = GbifDownload("name", "email")
        req.main_pred_type = "|"
        self.assertEqual(req.payload["predicate"]["type"], "or")

        # predicate addition
        req.add_predicate_dict({"type":"greaterThanOrEquals","key":"YEAR", "value":"2000"})
        self.assertEqual(
            req.payload["predicate"]["predicates"][0]["type"], "greaterThanOrEquals"
        )

    # mocking the request service
    requests.post = dummypost

    def test_post_download(self):
        req = GbifDownload("name", "email")
        req.add_iterative_predicate(
            "BASIS_OF_RECORD", ["FOSSIL_SPECIMEN", "LITERATURE"]
        )
        dl_key = req.post_download("name", "pwd")
        if not dl_key:
            raise KeyError(
                "You might have too many downloads running at the \
                            same time. Check your downloads page!"
            )

        while req.get_status() in ["PREPARING", "RUNNING"]:
            print("Preparing ...")
            time.sleep(10)
        self.assertIn(req.get_status(), ["SUCCEEDED", "KILLED"])


class TestDownload(unittest.TestCase):

    # mocking the request service
    requests.post = dummypost

    def test_single_predicate(self):
        dl_key, payload = download(
            "decimalLatitude > 50", user="dummy", email="dummy", pwd="dummy"
        )
        self.assertDictEqual(
            payload["predicate"]["predicates"][0],
            {"key": "DECIMAL_LATITUDE", "type": "greaterThan", "value": 50.0},
        )

        dl_key, payload = download(
            "basisOfRecord = LITERATURE", user="dummy", email="dummy", pwd="dummy"
        )
        self.assertDictEqual(
            payload["predicate"]["predicates"][0],
            {"key": "BASIS_OF_RECORD", "type": "equals", "value": "LITERATURE"},
        )

    def test_single_predicate_list(self):
        dl_key, payload = download(
            ["decimalLatitude > 50"], user="dummy", email="dummy", pwd="dummy"
        )

        self.assertDictEqual(
            payload["predicate"]["predicates"][0],
            {"key": "DECIMAL_LATITUDE", "type": "greaterThan", "value": 50.0},
        )

    def test_multiple_predicates(self):
        dl_key, payload = download(
            ["taxonKey = 7264332", "hasCoordinate = TRUE"],
            user="dummy",
            email="dummy",
            pwd="dummy",
        )
        temp_pred = payload["predicate"]["predicates"]
        self.assertIsInstance(temp_pred, list)
        self.assertEqual(len(temp_pred), 2)
        self.assertIsInstance(temp_pred[0], dict)
        self.assertIsInstance(temp_pred[1], dict)
        self.assertEqual(set(list(temp_pred[0].keys())), set(["key", "type", "value"]))
        self.assertEqual(set(list(temp_pred[1].keys())), set(["key", "type", "value"]))

    def test_alternative_main_type(self):
        dl_key, payload = download(
            ["depth = 80", "taxonKey = 2343454"],
            pred_type="or",
            user="dummy",
            email="dummy",
            pwd="dummy",
        )

        self.assertEqual(payload["predicate"]["type"], "or")

    def test_geometry_predicate(self):
        dl_key, payload = download(
            ["geometry within POLYGON((-82.7 36.9, -85.0 35.6, -81.0 33.5, -79.4 36.3, -79.4 36.3, -82.7 36.9))"], 
            user="dummy", email="dummy", pwd="dummy"
        )

        self.assertDictEqual(
            payload["predicate"]["predicates"][0],
            {"type": "within", "geometry": "POLYGON((-82.7 36.9, -85.0 35.6, -81.0 33.5, -79.4 36.3, -79.4 36.3, -82.7 36.9))"},
        )

    def test_taxonkey_integer_conversion(self):
        """Test that taxonKey values are converted to integers (issue #179)"""
        dl_key, payload = download(
            "taxonKey = 3119195",
            user="dummy",
            email="dummy",
            pwd="dummy",
        )
        # taxonKey value should be an integer, not a string
        self.assertDictEqual(
            payload["predicate"]["predicates"][0],
            {"key": "TAXON_KEY", "type": "equals", "value": 3119195},
        )
        self.assertIsInstance(payload["predicate"]["predicates"][0]["value"], int)

    def test_taxonkey_in_predicate_integer_conversion(self):
        """Test that taxonKey values in 'in' predicate are converted to integers"""
        dl_key, payload = download(
            'taxonKey in ["2387246", "2399391", "2364604"]',
            user="dummy",
            email="dummy",
            pwd="dummy",
        )
        # taxonKey values should be integers in the list
        self.assertDictEqual(
            payload["predicate"]["predicates"][0],
            {"key": "TAXON_KEY", "type": "in", "values": [2387246, 2399391, 2364604]},
        )
        for val in payload["predicate"]["predicates"][0]["values"]:
            self.assertIsInstance(val, int)

    def test_year_integer_conversion(self):
        """Test that year values are converted to integers"""
        dl_key, payload = download(
            "year = 2023",
            user="dummy",
            email="dummy",
            pwd="dummy",
        )
        self.assertDictEqual(
            payload["predicate"]["predicates"][0],
            {"key": "YEAR", "type": "equals", "value": 2023},
        )
        self.assertIsInstance(payload["predicate"]["predicates"][0]["value"], int)

    def test_depth_numeric_conversion(self):
        """Test that depth values are converted to float"""
        dl_key, payload = download(
            "depth = 80.5",
            user="dummy",
            email="dummy",
            pwd="dummy",
        )
        self.assertDictEqual(
            payload["predicate"]["predicates"][0],
            {"key": "DEPTH", "type": "equals", "value": 80.5},
        )
        self.assertIsInstance(payload["predicate"]["predicates"][0]["value"], float)

    def test_multiple_predicates_with_integer_keys(self):
        """Test multiple predicates with integer key conversion"""
        dl_key, payload = download(
            ["taxonKey = 7264332", "year = 2020"],
            user="dummy",
            email="dummy",
            pwd="dummy",
        )
        temp_pred = payload["predicate"]["predicates"]
        # Both values should be integers
        self.assertEqual(temp_pred[0]["value"], 7264332)
        self.assertEqual(temp_pred[1]["value"], 2020)
        self.assertIsInstance(temp_pred[0]["value"], int)
        self.assertIsInstance(temp_pred[1]["value"], int)
