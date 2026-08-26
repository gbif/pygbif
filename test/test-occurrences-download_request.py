import time
import requests
import unittest
import warnings
from unittest.mock import patch

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
        req.add_iterative_predicate("TAXONKEY", ["5WZLF", "75F9"])
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

    @patch('requests.post', side_effect=dummypost)
    def test_post_download(self, mock_post):
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

    @patch('requests.post', side_effect=dummypost)
    def test_single_predicate(self, mock_post):
        dl_key, payload = download(
            "decimalLatitude > 50", user="dummy", email="dummy", pwd="dummy"
        )
        self.assertDictEqual(
            payload["predicate"]["predicates"][0],
            {"key": "DECIMAL_LATITUDE", "type": "greaterThan", "value": "50"},
        )

        dl_key, payload = download(
            "basisOfRecord = LITERATURE", user="dummy", email="dummy", pwd="dummy"
        )
        self.assertDictEqual(
            payload["predicate"]["predicates"][0],
            {"key": "BASIS_OF_RECORD", "type": "equals", "value": "LITERATURE"},
        )

    @patch('requests.post', side_effect=dummypost)
    def test_single_predicate_list(self, mock_post):
        dl_key, payload = download(
            ["decimalLatitude > 50"], user="dummy", email="dummy", pwd="dummy"
        )

        self.assertDictEqual(
            payload["predicate"]["predicates"][0],
            {"key": "DECIMAL_LATITUDE", "type": "greaterThan", "value": "50"},
        )

    @patch('requests.post', side_effect=dummypost)
    def test_multiple_predicates(self, mock_post):
        dl_key, payload = download(
            ["taxonKey = 5WZLF", "hasCoordinate = TRUE"],
            user="dummy",
            email="dummy",
            pwd="dummy",
        )
        temp_pred = payload["predicate"]["predicates"]
        self.assertIsInstance(temp_pred, list)
        self.assertEqual(len(temp_pred), 2)
        self.assertIsInstance(temp_pred[0], dict)
        self.assertIsInstance(temp_pred[1], dict)
        # First predicate is taxonKey, should have checklistKey injected
        self.assertEqual(set(list(temp_pred[0].keys())), set(["key", "type", "value", "checklistKey"]))
        # Second predicate is hasCoordinate, should NOT have checklistKey
        self.assertEqual(set(list(temp_pred[1].keys())), set(["key", "type", "value"]))

    @patch('requests.post', side_effect=dummypost)
    def test_alternative_main_type(self, mock_post):
        dl_key, payload = download(
            ["depth = 80", "taxonKey = 7B3XY"],
            pred_type="or",
            user="dummy",
            email="dummy",
            pwd="dummy",
        )

        self.assertEqual(payload["predicate"]["type"], "or")

    @patch('requests.post', side_effect=dummypost)
    def test_geometry_predicate(self, mock_post):
        dl_key, payload = download(
            ["geometry within POLYGON((-82.7 36.9, -85.0 35.6, -81.0 33.5, -79.4 36.3, -79.4 36.3, -82.7 36.9))"], 
            user="dummy", email="dummy", pwd="dummy"
        )

        self.assertDictEqual(
            payload["predicate"]["predicates"][0],
            {"type": "within", "geometry": "POLYGON((-82.7 36.9, -85.0 35.6, -81.0 33.5, -79.4 36.3, -79.4 36.3, -82.7 36.9))"},
        )

    @patch('requests.post', side_effect=dummypost)
    def test_checklistkey_in_payload(self, mock_post):
        """Test that checklistKey parameter is included at both root and predicate levels"""
        checklist_uuid = "7ddf754f-d193-4cc9-b351-99906754a03b"
        
        dl_key, payload = download(
            "taxonKey = 5WZLF",
            checklistKey=checklist_uuid,
            user="dummy",
            email="dummy",
            pwd="dummy",
        )
        
        # checklistKey should be at root level
        self.assertIn("checklistKey", payload)
        self.assertEqual(payload["checklistKey"], checklist_uuid)
        
        # checklistKey should also be in predicates (for proper taxonomy resolution)
        self.assertIn("checklistKey", payload["predicate"]["predicates"][0])
        self.assertEqual(payload["predicate"]["predicates"][0]["checklistKey"], checklist_uuid)

    @patch('requests.post', side_effect=dummypost)
    def test_checklistkey_col_default_for_alphanumeric_keys(self, mock_post):
        """Test that COL Extended Release is used by default for alphanumeric taxon keys"""
        
        dl_key, payload = download(
            "taxonKey = 5WZLF",
            user="dummy",
            email="dummy",
            pwd="dummy",
        )
        
        # Should use COL Extended Release by default for alphanumeric keys
        self.assertIn("checklistKey", payload)
        self.assertEqual(payload["checklistKey"], "7ddf754f-d193-4cc9-b351-99906754a03b")

    @patch('requests.post', side_effect=dummypost)
    def test_checklistkey_with_multiple_predicates(self, mock_post):
        """Test that global checklistKey is at root level and injected into taxon predicates"""
        checklist_uuid = "7ddf754f-d193-4cc9-b351-99906754a03b"
        
        dl_key, payload = download(
            ["taxonKey = 5WZLF", "country = US"],
            checklistKey=checklist_uuid,
            user="dummy",
            email="dummy",
            pwd="dummy",
        )
        
        # checklistKey should be at root level
        self.assertIn("checklistKey", payload)
        self.assertEqual(payload["checklistKey"], checklist_uuid)
        
        # Should have 2 predicates
        self.assertEqual(len(payload["predicate"]["predicates"]), 2)
        
        # checklistKey should be in taxon predicate but NOT in country predicate
        taxon_pred = payload["predicate"]["predicates"][0]
        country_pred = payload["predicate"]["predicates"][1]
        self.assertIn("checklistKey", taxon_pred)
        self.assertEqual(taxon_pred["checklistKey"], checklist_uuid)
        self.assertNotIn("checklistKey", country_pred)

    @patch('requests.post', side_effect=dummypost)
    def test_checklistkey_with_dict_query(self, mock_post):
        """Test that global checklistKey works with dictionary queries"""
        checklist_uuid = "7ddf754f-d193-4cc9-b351-99906754a03b"
        
        query = {
            "type": "and",
            "predicates": [
                {"type": "equals", "key": "TAXON_KEY", "value": "5WZLF"},
                {"type": "equals", "key": "COUNTRY", "value": "US"}
            ]
        }
        
        dl_key, payload = download(
            query,
            checklistKey=checklist_uuid,
            user="dummy",
            email="dummy",
            pwd="dummy",
        )
        
        # checklistKey should be at root level
        self.assertIn("checklistKey", payload)
        self.assertEqual(payload["checklistKey"], checklist_uuid)
        
        # checklistKey should be in taxon predicate but not country predicate
        taxon_pred = payload["predicate"]["predicates"][0]
        country_pred = payload["predicate"]["predicates"][1]
        self.assertIn("checklistKey", taxon_pred)
        self.assertEqual(taxon_pred["checklistKey"], checklist_uuid)
        self.assertNotIn("checklistKey", country_pred)

    def test_gbif_download_class_with_checklistkey(self):
        """Test that GbifDownload class stores checklistKey at root level only"""
        checklist_uuid = "7ddf754f-d193-4cc9-b351-99906754a03b"
        
        req = GbifDownload("name", "email", checklistKey=checklist_uuid)
        
        # checklistKey should be at root level
        self.assertIn("checklistKey", req.payload)
        self.assertEqual(req.payload["checklistKey"], checklist_uuid)
        
    @patch('requests.post', side_effect=dummypost)
    def test_manual_checklistkey_in_predicate(self, mock_post):
        """Test that checklistKey can be used in predicates for search filtering
        
        The checklistKey parameter can be included within individual predicates
        to specify the taxonomy to be used for filtering occurrence records.
        """
        checklist_uuid = "7ddf754f-d193-4cc9-b351-99906754a03b"
        another_checklist = "12345678-1234-1234-1234-123456789abc"
        
        # User manually specifies checklistKey in a predicate for search filtering
        query = {
            "type": "equals",
            "key": "TAXON_KEY",
            "value": "5WZLF",
            "checklistKey": another_checklist  # Predicate-level for filtering
        }
        
        dl_key, payload = download(
            query,
            checklistKey=checklist_uuid,  # Global checklistKey (root level)
            user="dummy",
            email="dummy",
            pwd="dummy",
        )
        
        # Global checklistKey should be at root level
        self.assertIn("checklistKey", payload)
        self.assertEqual(payload["checklistKey"], checklist_uuid)
        
        # Predicate-level checklistKey should be preserved for filtering
        self.assertIn("checklistKey", payload["predicate"])
        self.assertEqual(payload["predicate"]["checklistKey"], another_checklist)

    def test_gbif_download_class_without_checklistkey(self):
        """Test that GbifDownload class doesn't include checklistKey when not provided"""
        
        req = GbifDownload("name", "email")
        
        self.assertNotIn("checklistKey", req.payload)

    @patch('requests.post', side_effect=dummypost)
    def test_numeric_key_deprecation_warning(self, mock_post):
        """Test that numeric taxon keys trigger deprecation warning and use GBIF Backbone"""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            dl_key, payload = download(
                "taxonKey = 3119195",
                user="dummy",
                email="dummy",
                pwd="dummy",
            )
            
            # Should have a deprecation warning
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))
            self.assertIn("Numeric taxon keys", str(w[0].message))
            
            # Should include checklistKey at root (COL default) and predicate (GBIF Backbone)
            self.assertIn("checklistKey", payload)
            self.assertEqual(payload["checklistKey"], "7ddf754f-d193-4cc9-b351-99906754a03b")  # COL at root
            # Predicate should have GBIF Backbone
            self.assertIn("checklistKey", payload["predicate"]["predicates"][0])
            self.assertEqual(payload["predicate"]["predicates"][0]["checklistKey"], "d7dddbf4-2cf0-4f39-9b2a-bb099caae36c")

    @patch('requests.post', side_effect=dummypost)
    def test_numeric_key_explicit_checklistkey_no_warning(self, mock_post):
        """Test that explicit checklistKey=None with numeric keys doesn't warn"""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            dl_key, payload = download(
                "taxonKey = 3119195",
                checklistKey=None,
                user="dummy",
                email="dummy",
                pwd="dummy",
            )
            
            # Should NOT have a deprecation warning (user explicitly set checklistKey)
            self.assertEqual(len(w), 0)
            
            # Should NOT include checklistKey in payload
            self.assertNotIn("checklistKey", payload)

    @patch('requests.post', side_effect=dummypost)
    def test_numeric_specieskey_deprecation_warning(self, mock_post):
        """Test that numeric speciesKey also triggers the warning"""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            dl_key, payload = download(
                "speciesKey = 2435098",
                user="dummy",
                email="dummy",
                pwd="dummy",
            )
            
            # Should have a deprecation warning
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))
            
            # Should include checklistKey at root (COL default) and predicate (GBIF Backbone)
            self.assertIn("checklistKey", payload)
            self.assertEqual(payload["checklistKey"], "7ddf754f-d193-4cc9-b351-99906754a03b")  # COL at root
            self.assertIn("checklistKey", payload["predicate"]["predicates"][0])
            self.assertEqual(payload["predicate"]["predicates"][0]["checklistKey"], "d7dddbf4-2cf0-4f39-9b2a-bb099caae36c")

    @patch('requests.post', side_effect=dummypost)
    def test_numeric_key_in_dict_query_deprecation(self, mock_post):
        """Test that numeric keys in dict queries also trigger warning"""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            query = {
                "type": "equals",
                "key": "TAXON_KEY",
                "value": "7264332"
            }
            
            dl_key, payload = download(
                query,
                user="dummy",
                email="dummy",
                pwd="dummy",
            )
            
            # Should have a deprecation warning
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))
            
            # Should include checklistKey at root (COL default) and predicate (GBIF Backbone)
            self.assertIn("checklistKey", payload)
            self.assertEqual(payload["checklistKey"], "7ddf754f-d193-4cc9-b351-99906754a03b")  # COL at root
            self.assertIn("checklistKey", payload["predicate"])
            self.assertEqual(payload["predicate"]["checklistKey"], "d7dddbf4-2cf0-4f39-9b2a-bb099caae36c")

    @patch('requests.post', side_effect=dummypost)
    def test_multiple_predicates_with_numeric_key(self, mock_post):
        """Test that numeric keys in one of multiple predicates triggers warning"""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            dl_key, payload = download(
                ["taxonKey = 7264332", "country = US"],
                user="dummy",
                email="dummy",
                pwd="dummy",
            )
            
            # Should have a deprecation warning
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))
            
            # Should include checklistKey at root (COL default)
            self.assertIn("checklistKey", payload)
            self.assertEqual(payload["checklistKey"], "7ddf754f-d193-4cc9-b351-99906754a03b")  # COL at root
            # Taxon predicate should have GBIF Backbone
            self.assertIn("checklistKey", payload["predicate"]["predicates"][0])
            self.assertEqual(payload["predicate"]["predicates"][0]["checklistKey"], "d7dddbf4-2cf0-4f39-9b2a-bb099caae36c")

    @patch('requests.post', side_effect=dummypost)
    def test_predicate_level_checklistkey_no_warning(self, mock_post):
        """Test that numeric keys with predicate-level checklistKey don't trigger warning"""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            # Predicate with numeric key but explicit checklistKey at predicate level
            query = {
                "type": "equals",
                "key": "TAXON_KEY",
                "value": "3119195",  # Numeric key
                "checklistKey": "d7dddbf4-2cf0-4f39-9b2a-bb099caae36c"  # Explicit GBIF Backbone
            }
            
            dl_key, payload = download(
                query,
                user="dummy",
                email="dummy",
                pwd="dummy",
            )
            
            # Should NOT have a deprecation warning (predicate has explicit checklistKey)
            deprecation_warnings = [warning for warning in w if issubclass(warning.category, DeprecationWarning)]
            self.assertEqual(len(deprecation_warnings), 0)
            
            # Should have COL as default checklistKey at root level
            self.assertEqual(payload["checklistKey"], "7ddf754f-d193-4cc9-b351-99906754a03b")


