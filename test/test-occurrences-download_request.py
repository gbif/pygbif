
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
        # TODO

    def test_lookup_predicates(self):
        """different lookups checked"""
        req = GbifDownload("name", "email")
        req.main_pred_type = "|"
        self.assertEqual(req.payload['predicate']['type'], "or")

        # ADAPT -> hier voor een gewoon predicate doen!
        req.main_pred_type = ">="
        self.assertEqual(req.payload['predicate']['type'],
                         "greaterThanOrEquals")

