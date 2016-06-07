import unittest

from pygbif.occurrences.download import GbifDownload


class TestGbifClass(unittest.TestCase):
    def test_gbif_creation(self):
        """test the creation of the predicate class"""

        req = GbifDownload("name", "email")
        self.assertIsInstance(req.payload, dict)
        self.assertDictEqual(req.payload, {'created': 2016, 'creator': 'name',
                                           'notification_address': ['email'],
                                           'predicate': {'predicates': [],
                                                         'type': 'and'},
                                           'send_notification': 'true'})
        self.assertIsNone(req.request_id)

    def test_alternative_main_type(self):
        """test the addition of another predicate combiner"""
        req = GbifDownload("name", "email")
        req.main_pred_type = "or"
        self.assertIsInstance(req.payload, dict)
        self.assertDictEqual(req.payload, {'created': 2016, 'creator': 'name',
                                           'notification_address': ['email'],
                                           'predicate': {'predicates': [],
                                                         'type': 'or'},
                                           'send_notification': 'true'})

    def test_add_predicate(self):
        """test the predicate addition"""
        req = GbifDownload("name", "email")
        req.add_predicate("COUNTRY", "BE", "equals")
        self.assertIsInstance(req.payload["predicate"]["predicates"], list)
        self.assertEquals(len(req.payload["predicate"]["predicates"]), 1)
        self.assertIsInstance(req.payload["predicate"]["predicates"][0], dict)
        self.assertDictEqual(req.payload["predicate"]["predicates"][0],
                             {'key': 'COUNTRY',
                              'type': 'equals',
                              'value': 'BE'})

    def test_add_iterative_predicate(self):
        """the the predicate addition of an iterative sequence"""
        req = GbifDownload("name", "email")
        req.add_iterative_predicate("TAXONKEY", [3189866, 2498252])
        self.assertIsInstance(req.payload["predicate"]["predicates"], list)
        self.assertEquals(len(req.payload["predicate"]["predicates"]), 1)
        self.assertIsInstance(req.payload["predicate"]["predicates"][0], dict)

        temp_pred = req.payload["predicate"]["predicates"][0]["predicates"]
        self.assertIsInstance(temp_pred, list)
        self.assertEquals(len(temp_pred), 2)
        self.assertIsInstance(temp_pred[0], dict)

        self.assertEquals(set(list(temp_pred[0].keys())),
                             set(['key', 'type', 'value']))
        self.assertEquals(req.payload["predicate"]["predicates"][0]['type'],
                          'or')

    def test_add_geometry(self):
        """check predicate after adding a geometry"""
        req = GbifDownload("name", "email")
        req.add_geometry(
            'POLYGON((-14.06 42.55, 9.84 38.27, -7.03 26.43, -14.06 42.55))')
        self.assertIsInstance(req.payload["predicate"]["predicates"], list)
        self.assertEquals(len(req.payload["predicate"]["predicates"]), 1)
        self.assertEquals(
            set(req.payload["predicate"]["predicates"][0].keys()),
            set(['type', 'geometry']))

    def test_lookup_predicates(self):
        """different lookups checked"""
        # main combination predicate
        req = GbifDownload("name", "email")
        req.main_pred_type = "|"
        self.assertEqual(req.payload['predicate']['type'], "or")

        # predicate addition
        req.add_predicate("YEAR", "2000", ">=")
        self.assertEqual(req.payload["predicate"]["predicates"][0]["type"],
                         "greaterThanOrEquals")
