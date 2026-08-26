"""Live tests for occurrences.download with real API requests
These tests make actual requests to the GBIF API and require valid credentials.
They verify the COL Extended Release migration and backward compatibility.

NOTE: These tests use VCR cassettes to record API responses. Once cassettes are
recorded, tests can run without credentials. To re-record cassettes, delete the
cassette files and run with valid GBIF credentials.

These tests are slow (~2-3 seconds per test) due to API rate limits and 
download cancellation delays. GBIF limits users to 3 simultaneous downloads.
"""
import pytest
import os
import warnings
import time
import vcr
from pygbif import occurrences as occ

# Skip these tests if credentials are not available
# Note: In CI, credentials are provided via secrets, so tests will run
SKIP_LIVE_TESTS = not all([
    os.getenv("GBIF_USER"),
    os.getenv("GBIF_PWD"), 
    os.getenv("GBIF_EMAIL")
])

SKIP_REASON = "Live tests require GBIF_USER, GBIF_PWD, and GBIF_EMAIL environment variables"


@pytest.mark.skipif(SKIP_LIVE_TESTS, reason=SKIP_REASON)
class TestDownloadLive:
    """Live tests that make real download requests"""
    
    def setup_method(self):
        """Store download keys for cleanup"""
        self.download_keys = []
        # Add delay to avoid hitting GBIF's 3 simultaneous download limit
        # Only relevant when running live tests (not when using VCR cassettes)
        time.sleep(2)
    
    def teardown_method(self):
        """Cancel all downloads created during tests"""
        for key in self.download_keys:
            try:
                occ.download_cancel(key)
                print(f"Cancelled download: {key}")
            except Exception as e:
                print(f"Failed to cancel download {key}: {e}")
        # Add delay after cancellation to let API process
        # Only relevant when running live tests
        if self.download_keys:
            time.sleep(1)
    
    @vcr.use_cassette("test/vcr_cassettes/test_download_live_col_default.yaml", filter_headers=["authorization"])
    def test_col_default_with_alphanumeric_key(self):
        """Test that COL Extended Release is used by default with alphanumeric taxon keys"""
        # Use a COL alphanumeric key
        download_key, payload = occ.download(
            "taxonKey = 5WZLF"  # COL Extended Release key
        )
        self.download_keys.append(download_key)
        
        # Verify the download was created
        assert download_key is not None
        assert len(download_key) > 0
        
        # Verify payload includes COL checklistKey at ROOT level
        assert "checklistKey" in payload
        assert payload["checklistKey"] == "7ddf754f-d193-4cc9-b351-99906754a03b"
        
        # Verify checklistKey is also injected at PREDICATE level
        assert "predicate" in payload
        assert "predicates" in payload["predicate"]
        taxon_predicate = payload["predicate"]["predicates"][0]
        assert "checklistKey" in taxon_predicate
        assert taxon_predicate["checklistKey"] == "7ddf754f-d193-4cc9-b351-99906754a03b"
        
        print(f"✓ COL default test passed (both root and predicate levels). Download key: {download_key}")
    
    @vcr.use_cassette("test/vcr_cassettes/test_download_live_numeric_key.yaml", filter_headers=["authorization"])
    def test_numeric_key_automatic_gbif_backbone(self):
        """Test that numeric keys get GBIF Backbone at predicate level with COL XR at root (default)"""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            # Use a numeric key (GBIF Backbone)
            download_key, payload = occ.download(
                "taxonKey = 2435098"  # Numeric key
            )
            self.download_keys.append(download_key)
            
            # Verify deprecation warning was issued
            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)
            assert "Numeric taxon keys" in str(w[0].message)
            
            # Verify the download was created
            assert download_key is not None
            assert len(download_key) > 0
            
            # Verify payload includes COL XR at ROOT level (always default)
            assert "checklistKey" in payload
            assert payload["checklistKey"] == "7ddf754f-d193-4cc9-b351-99906754a03b"
            
            # Verify checklistKey is also injected at PREDICATE level (GBIF Backbone for numeric value)
            assert "predicate" in payload
            assert "predicates" in payload["predicate"]
            taxon_predicate = payload["predicate"]["predicates"][0]
            assert "checklistKey" in taxon_predicate
            assert taxon_predicate["checklistKey"] == "d7dddbf4-2cf0-4f39-9b2a-bb099caae36c"
            
            print(f"✓ Numeric key test passed (COL at root, GBIF Backbone at predicate). Download key: {download_key}")
            print(f"  Warning message: {w[0].message}")
    
    @vcr.use_cassette("test/vcr_cassettes/test_download_live_numeric_mixed.yaml", filter_headers=["authorization"])
    def test_numeric_key_with_mixed_predicates(self):
        """Test that numeric keys with non-taxon predicates use COL XR at root, GBIF Backbone at predicate"""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            # Use numeric key with another predicate (no explicit checklistKey)
            download_key, payload = occ.download(
                ["taxonKey = 2435098", "country = VA"]  # Numeric key + country
            )
            self.download_keys.append(download_key)
            
            # Verify deprecation warning was issued
            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)
            assert "Numeric taxon keys" in str(w[0].message)
            
            # Verify the download was created
            assert download_key is not None
            assert len(download_key) > 0
            
            # Verify payload includes COL XR at ROOT level (always default)
            assert "checklistKey" in payload
            assert payload["checklistKey"] == "7ddf754f-d193-4cc9-b351-99906754a03b"
            
            # Verify both predicates are present
            assert "predicate" in payload
            assert "predicates" in payload["predicate"]
            assert len(payload["predicate"]["predicates"]) == 2
            
            # Verify checklistKey is injected at PREDICATE level for taxon key
            predicates = payload["predicate"]["predicates"]
            taxon_pred = [p for p in predicates if p.get("key") == "TAXON_KEY"][0]
            country_pred = [p for p in predicates if p.get("key") == "COUNTRY"][0]
            
            # Verify taxon predicate has GBIF Backbone checklistKey (numeric value)
            assert taxon_pred["key"] == "TAXON_KEY"
            assert taxon_pred["value"] == "2435098"
            assert "checklistKey" in taxon_pred
            assert taxon_pred["checklistKey"] == "d7dddbf4-2cf0-4f39-9b2a-bb099caae36c"
            
            # Verify country predicate has no checklistKey
            assert country_pred["key"] == "COUNTRY"
            assert country_pred["value"] == "VA"
            assert "checklistKey" not in country_pred
            
            print(f"✓ Numeric mixed predicates test passed (COL at root, value-based at predicate). Download key: {download_key}")
            print(f"  Warning message: {w[0].message}")
    
    @vcr.use_cassette("test/vcr_cassettes/test_download_live_explicit_col.yaml", filter_headers=["authorization"])
    def test_explicit_col_checklist(self):
        """Test explicitly specifying COL Extended Release checklistKey"""
        download_key, payload = occ.download(
            "country = US",
            checklistKey="7ddf754f-d193-4cc9-b351-99906754a03b"
        )
        self.download_keys.append(download_key)
        
        # Verify the download was created
        assert download_key is not None
        assert len(download_key) > 0
        
        # Verify payload includes COL checklistKey
        assert "checklistKey" in payload
        assert payload["checklistKey"] == "7ddf754f-d193-4cc9-b351-99906754a03b"
        
        print(f"✓ Explicit COL test passed. Download key: {download_key}")
    
    @vcr.use_cassette("test/vcr_cassettes/test_download_live_explicit_backbone.yaml", filter_headers=["authorization"])
    def test_explicit_gbif_backbone_no_warning(self):
        """Test that explicitly setting GBIF Backbone checklistKey with numeric keys doesn't warn"""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            # Use numeric key with explicit GBIF Backbone checklistKey
            download_key, payload = occ.download(
                "taxonKey = 2435098",
                checklistKey="d7dddbf4-2cf0-4f39-9b2a-bb099caae36c"
            )
            self.download_keys.append(download_key)
            
            # Verify NO deprecation warning (user made explicit choice)
            deprecation_warnings = [warn for warn in w if issubclass(warn.category, DeprecationWarning)]
            assert len(deprecation_warnings) == 0
            
            # Verify the download was created
            assert download_key is not None
            assert len(download_key) > 0
            
            # Verify payload includes GBIF Backbone checklistKey at ROOT level
            assert "checklistKey" in payload
            assert payload["checklistKey"] == "d7dddbf4-2cf0-4f39-9b2a-bb099caae36c"
            
            # Verify checklistKey is also at PREDICATE level
            taxon_predicate = payload["predicate"]["predicates"][0]
            assert "checklistKey" in taxon_predicate
            assert taxon_predicate["checklistKey"] == "d7dddbf4-2cf0-4f39-9b2a-bb099caae36c"
            
            print(f"✓ Explicit GBIF Backbone test passed (both levels, no warning). Download key: {download_key}")
    
    @vcr.use_cassette("test/vcr_cassettes/test_download_live_explicit_none.yaml", filter_headers=["authorization"])
    def test_explicit_none_no_checklistkey(self):
        """Test that explicitly setting checklistKey=None results in no checklistKey anywhere"""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            # Use explicit checklistKey=None (backward compatibility - no checklistKey at all)
            download_key, payload = occ.download(
                "country = VA",
                checklistKey=None
            )
            self.download_keys.append(download_key)
            
            # Verify NO deprecation warning (user made explicit choice)
            deprecation_warnings = [warn for warn in w if issubclass(warn.category, DeprecationWarning)]
            assert len(deprecation_warnings) == 0
            
            # Verify the download was created
            assert download_key is not None
            assert len(download_key) > 0
            
            # Verify payload does NOT include checklistKey at ROOT level
            assert "checklistKey" not in payload
            
            # Verify no checklistKey at PREDICATE level either
            predicates = payload["predicate"]["predicates"]
            for pred in predicates:
                assert "checklistKey" not in pred
            
            print(f"✓ Explicit None test passed (no checklistKey anywhere). Download key: {download_key}")
    
    @vcr.use_cassette("test/vcr_cassettes/test_download_live_mixed_predicates.yaml", filter_headers=["authorization"])
    def test_mixed_predicates_with_col(self):
        """Test multiple predicates with COL keys work correctly"""
        download_key, payload = occ.download(
            ["taxonKey = 5WZLF", "country = US", "hasCoordinate = TRUE"]
        )
        self.download_keys.append(download_key)
        
        # Verify the download was created
        assert download_key is not None
        assert len(download_key) > 0
        
        # Verify payload includes COL checklistKey
        assert "checklistKey" in payload
        assert payload["checklistKey"] == "7ddf754f-d193-4cc9-b351-99906754a03b"
        
        # Verify all predicates are present
        assert "predicate" in payload
        assert "predicates" in payload["predicate"]
        assert len(payload["predicate"]["predicates"]) == 3
        
        # Verify checklistKey is only injected into taxon predicate, not others
        predicates = payload["predicate"]["predicates"]
        taxon_pred = [p for p in predicates if p.get("key") == "TAXON_KEY"][0]
        country_pred = [p for p in predicates if p.get("key") == "COUNTRY"][0]
        coord_pred = [p for p in predicates if p.get("key") == "HAS_COORDINATE"][0]
        
        # Verify taxon predicate has correct key, value, and checklistKey
        assert taxon_pred["key"] == "TAXON_KEY"
        assert taxon_pred["value"] == "5WZLF"
        assert "checklistKey" in taxon_pred
        assert taxon_pred["checklistKey"] == "7ddf754f-d193-4cc9-b351-99906754a03b"
        
        # Verify country predicate has correct key and value (no checklistKey)
        assert country_pred["key"] == "COUNTRY"
        assert country_pred["value"] == "US"
        assert "checklistKey" not in country_pred
        
        # Verify coordinate predicate has correct key and value (no checklistKey)
        assert coord_pred["key"] == "HAS_COORDINATE"
        assert coord_pred["value"] == "TRUE"
        assert "checklistKey" not in coord_pred
        
        print(f"✓ Mixed predicates test passed (selective predicate injection). Download key: {download_key}")
    
    @vcr.use_cassette("test/vcr_cassettes/test_download_live_dict_predicate.yaml", filter_headers=["authorization"])
    def test_dict_predicate_with_col(self):
        """Test dict-style predicates with COL keys work correctly"""
        query = {
            "type": "and",
            "predicates": [
                {
                    "type": "equals",
                    "key": "TAXON_KEY",
                    "value": "5WZLF"
                },
                {
                    "type": "equals",
                    "key": "COUNTRY",
                    "value": "US"
                }
            ]
        }
        
        download_key, payload = occ.download(query)
        self.download_keys.append(download_key)
        
        # Verify the download was created
        assert download_key is not None
        assert len(download_key) > 0
        
        # Verify payload includes COL checklistKey at ROOT level
        assert "checklistKey" in payload
        assert payload["checklistKey"] == "7ddf754f-d193-4cc9-b351-99906754a03b"
        
        # Verify checklistKey is injected at PREDICATE level for taxon key
        predicates = payload["predicate"]["predicates"]
        taxon_pred = [p for p in predicates if p.get("key") == "TAXON_KEY"][0]
        country_pred = [p for p in predicates if p.get("key") == "COUNTRY"][0]
        
        assert "checklistKey" in taxon_pred
        assert taxon_pred["checklistKey"] == "7ddf754f-d193-4cc9-b351-99906754a03b"
        assert "checklistKey" not in country_pred  # Should NOT be in non-taxon predicates
        
        print(f"✓ Dict predicate test passed (both root and predicate levels). Download key: {download_key}")
    
    @vcr.use_cassette("test/vcr_cassettes/test_download_live_predicate_checklist.yaml", filter_headers=["authorization"])
    def test_predicate_level_checklistkey(self):
        """Test predicate-level checklistKey works with real API"""
        query = {
            "type": "equals",
            "key": "TAXON_KEY",
            "value": "5WZLF",
            "checklistKey": "7ddf754f-d193-4cc9-b351-99906754a03b"
        }
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            download_key, payload = occ.download(query)
            self.download_keys.append(download_key)
            
            # Verify NO warning (predicate has explicit checklistKey)
            deprecation_warnings = [warn for warn in w if issubclass(warn.category, DeprecationWarning)]
            assert len(deprecation_warnings) == 0
            
            # Verify the download was created
            assert download_key is not None
            assert len(download_key) > 0
            
            # Verify root-level COL checklistKey is present
            assert "checklistKey" in payload
            assert payload["checklistKey"] == "7ddf754f-d193-4cc9-b351-99906754a03b"
            
            print(f"✓ Predicate-level checklistKey test passed. Download key: {download_key}")
    
    @vcr.use_cassette("test/vcr_cassettes/test_download_live_status_check.yaml", filter_headers=["authorization"])
    def test_download_status_check(self):
        """Test that we can check status of a download with COL"""
        # Create a download
        download_key, payload = occ.download("taxonKey = 5WZLF")
        self.download_keys.append(download_key)
        
        # Check status (should be PREPARING or RUNNING)
        status = occ.download_meta(download_key)
        
        assert status is not None
        assert "status" in status
        assert status["status"] in ["PREPARING", "RUNNING", "SUCCEEDED", "CANCELLED", "FAILED"]
        
        print(f"✓ Status check test passed. Download key: {download_key}, Status: {status['status']}")
    
    @vcr.use_cassette("test/vcr_cassettes/test_download_live_complex_predicates.yaml", filter_headers=["authorization"])
    def test_complex_mixed_predicates_with_or(self):
        """Test complex predicates with OR logic, mixed numeric/alphanumeric keys, and nested structures
        
        This test validates:
        - OR and AND logic in nested predicates
        - Both numeric (GBIF Backbone) and alphanumeric (COL) taxon keys
        - Automatic COL XR for alphanumeric values, GBIF Backbone for numeric values
        - Each predicate gets appropriate checklistKey based on its value
        - Explicit checklistKey preservation on predicates that have them
        - Multiple rank keys (TAXON_KEY, SPECIES_KEY, FAMILY_KEY, GENUS_KEY)
        - Non-taxon predicates (COUNTRY, HAS_COORDINATE, BASIS_OF_RECORD)
        - Selective checklistKey injection (only on taxon predicates)
        """
        # Build a complex query with:
        # - OR and AND logic
        # - Both numeric (GBIF Backbone) and alphanumeric (COL) taxon keys
        # - Numeric key WITH explicit checklistKey (SPECIES_KEY) - preserves explicit value
        # - Numeric key WITHOUT explicit checklistKey (TAXON_KEY) - gets GBIF Backbone auto-injected
        # - Alphanumeric keys WITHOUT explicit checklistKey - get COL XR auto-injected
        # - Multiple rank keys (TAXON_KEY, SPECIES_KEY, FAMILY_KEY, GENUS_KEY)
        # - Non-taxon predicates (COUNTRY, HAS_COORDINATE, BASIS_OF_RECORD)
        # - Nested predicate structures
        query = {
            "type": "and",
            "predicates": [
                # OR block with mixed numeric and alphanumeric keys
                {
                    "type": "or",
                    "predicates": [
                        # Alphanumeric COL key - should auto-get COL checklistKey
                        {
                            "type": "equals",
                            "key": "TAXON_KEY",
                            "value": "5WZLF"
                        },
                        # Numeric GBIF Backbone key with explicit checklistKey (preserves it)
                        {
                            "type": "equals",
                            "key": "SPECIES_KEY",
                            "value": "2435098",
                            "checklistKey": "d7dddbf4-2cf0-4f39-9b2a-bb099caae36c"
                        },
                        # Another alphanumeric key - should auto-get COL checklistKey
                        {
                            "type": "equals",
                            "key": "FAMILY_KEY",
                            "value": "623LY"
                        },
                        # Numeric key WITHOUT explicit checklistKey - should auto-get GBIF Backbone
                        {
                            "type": "equals",
                            "key": "TAXON_KEY",
                            "value": "3119195"  # Numeric Plantae key
                        }
                    ]
                },
                # Non-taxon predicate - should NOT get checklistKey
                {
                    "type": "equals",
                    "key": "COUNTRY",
                    "value": "VA"
                },
                # Another OR block with mixed predicates
                {
                    "type": "or",
                    "predicates": [
                        {
                            "type": "equals",
                            "key": "HAS_COORDINATE",
                            "value": "TRUE"
                        },
                        {
                            "type": "equals",
                            "key": "GENUS_KEY",
                            "value": "5WZ4Y"  # COL key
                        }
                    ]
                },
                # Basis of record - non-taxon
                {
                    "type": "equals",
                    "key": "BASIS_OF_RECORD",
                    "value": "PRESERVED_SPECIMEN"
                }
            ]
        }
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            download_key, payload = occ.download(query)
            self.download_keys.append(download_key)
            
            # Warning expected because of numeric key without explicit checklistKey
            deprecation_warnings = [warn for warn in w if issubclass(warn.category, DeprecationWarning)]
            assert len(deprecation_warnings) == 1
            assert "Numeric taxon keys" in str(deprecation_warnings[0].message)
            
            # Verify the download was created
            assert download_key is not None
            assert len(download_key) > 0
            
            # Verify payload includes COL XR at ROOT level (always default)
            assert "checklistKey" in payload
            assert payload["checklistKey"] == "7ddf754f-d193-4cc9-b351-99906754a03b"
            
            # Navigate to first OR block
            first_or = payload["predicate"]["predicates"][0]
            assert first_or["type"] == "or"
            
            # Check TAXON_KEY (alphanumeric gets COL XR automatically)
            taxon_pred = first_or["predicates"][0]
            assert taxon_pred["key"] == "TAXON_KEY"
            assert taxon_pred["value"] == "5WZLF"
            assert "checklistKey" in taxon_pred
            assert taxon_pred["checklistKey"] == "7ddf754f-d193-4cc9-b351-99906754a03b"
            
            # Check SPECIES_KEY (numeric with explicit) kept its explicit GBIF Backbone
            species_pred = first_or["predicates"][1]
            assert species_pred["key"] == "SPECIES_KEY"
            assert species_pred["value"] == "2435098"
            assert "checklistKey" in species_pred
            assert species_pred["checklistKey"] == "d7dddbf4-2cf0-4f39-9b2a-bb099caae36c"
            
            # Check FAMILY_KEY (alphanumeric gets COL XR automatically)
            family_pred = first_or["predicates"][2]
            assert family_pred["key"] == "FAMILY_KEY"
            assert family_pred["value"] == "623LY"
            assert "checklistKey" in family_pred
            assert family_pred["checklistKey"] == "7ddf754f-d193-4cc9-b351-99906754a03b"
            
            # Check numeric TAXON_KEY (no explicit checklistKey) got GBIF Backbone auto-injected
            numeric_taxon_pred = first_or["predicates"][3]
            assert numeric_taxon_pred["key"] == "TAXON_KEY"
            assert numeric_taxon_pred["value"] == "3119195"
            assert "checklistKey" in numeric_taxon_pred
            assert numeric_taxon_pred["checklistKey"] == "d7dddbf4-2cf0-4f39-9b2a-bb099caae36c"
            
            # Check COUNTRY (non-taxon) has NO checklistKey
            country_pred = payload["predicate"]["predicates"][1]
            assert country_pred["key"] == "COUNTRY"
            assert country_pred["value"] == "VA"
            assert "checklistKey" not in country_pred
            
            # Navigate to second OR block
            second_or = payload["predicate"]["predicates"][2]
            assert second_or["type"] == "or"
            
            # Check HAS_COORDINATE (non-taxon) has NO checklistKey
            coord_pred = second_or["predicates"][0]
            assert coord_pred["key"] == "HAS_COORDINATE"
            assert coord_pred["value"] == "TRUE"
            assert "checklistKey" not in coord_pred
            
            # Check GENUS_KEY (alphanumeric gets COL XR automatically)
            genus_pred = second_or["predicates"][1]
            assert genus_pred["key"] == "GENUS_KEY"
            assert genus_pred["value"] == "5WZ4Y"
            assert "checklistKey" in genus_pred
            assert genus_pred["checklistKey"] == "7ddf754f-d193-4cc9-b351-99906754a03b"
            
            # Check BASIS_OF_RECORD (non-taxon) has NO checklistKey
            basis_pred = payload["predicate"]["predicates"][3]
            assert basis_pred["key"] == "BASIS_OF_RECORD"
            assert basis_pred["value"] == "PRESERVED_SPECIMEN"
            assert "checklistKey" not in basis_pred
            
            print(f"✓ Complex mixed predicates test passed (OR logic, auto-detected numeric keys, mixed taxonomies, nested structures). Download key: {download_key}")
            print(f"  Warning message: {deprecation_warnings[0].message}")

    @vcr.use_cassette("test/vcr_cassettes/test_download_live_in_predicates.yaml", filter_headers=["authorization"])
    def test_in_predicates_with_multiple_taxon_keys(self):
        """Test 'in' predicates with multiple taxon keys - alphanumeric, numeric, and explicit checklistKey"""
        # Build a complex query with three "in" predicates:
        # 1. Alphanumeric keys -> should inject COL XR
        # 2. Numeric keys -> should inject GBIF Backbone
        # 3. Explicit checklistKey -> should be preserved
        query = {
            "type": "and",
            "predicates": [
                # 1. IN predicate with alphanumeric COL keys (should get COL XR injected)
                {
                    "type": "in",
                    "key": "TAXON_KEY",
                    "values": ["5WZLF", "623LY", "5WZ4Y"]  # All alphanumeric
                },
                # 2. IN predicate with numeric GBIF Backbone keys (should get GBIF Backbone injected)
                {
                    "type": "in",
                    "key": "SPECIES_KEY",
                    "values": ["2435098", "3119195"]  # All numeric
                },
                # 3. IN predicate with explicit checklistKey (should be preserved)
                {
                    "type": "in",
                    "key": "GENUS_KEY",
                    "values": ["5WZMD", "5WZ8T"],
                    "checklistKey": "7ddf754f-d193-4cc9-b351-99906754a03b"  # Explicit
                },
                # 4. Non-taxon predicate (should have no checklistKey)
                {
                    "type": "equals",
                    "key": "COUNTRY",
                    "value": "US"
                }
            ]
        }
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            download_key, payload = occ.download(query)
            
            # Cancel the download immediately to avoid hitting limits
            time.sleep(1)
            occ.download_cancel(download_key)
            
            # Should warn about numeric keys
            deprecation_warnings = [warning for warning in w if issubclass(warning.category, DeprecationWarning)]
            assert len(deprecation_warnings) == 1
            assert "Numeric taxon keys detected" in str(deprecation_warnings[0].message)
            
            # Verify the download was created
            assert download_key is not None
            assert len(download_key) > 0
            
            # Verify payload includes COL XR at ROOT level (always default)
            assert "checklistKey" in payload
            assert payload["checklistKey"] == "7ddf754f-d193-4cc9-b351-99906754a03b"
            
            # Verify the predicates structure
            assert "predicate" in payload
            assert "predicates" in payload["predicate"]
            predicates = payload["predicate"]["predicates"]
            assert len(predicates) == 4
            
            # 1. Check first IN predicate with alphanumeric values -> COL XR injected
            taxon_in_pred = predicates[0]
            assert taxon_in_pred["type"] == "in"
            assert taxon_in_pred["key"] == "TAXON_KEY"
            assert taxon_in_pred["values"] == ["5WZLF", "623LY", "5WZ4Y"]
            assert "checklistKey" in taxon_in_pred
            assert taxon_in_pred["checklistKey"] == "7ddf754f-d193-4cc9-b351-99906754a03b"  # COL XR
            
            # 2. Check second IN predicate with numeric values -> GBIF Backbone injected
            species_in_pred = predicates[1]
            assert species_in_pred["type"] == "in"
            assert species_in_pred["key"] == "SPECIES_KEY"
            assert species_in_pred["values"] == ["2435098", "3119195"]
            assert "checklistKey" in species_in_pred
            assert species_in_pred["checklistKey"] == "d7dddbf4-2cf0-4f39-9b2a-bb099caae36c"  # GBIF Backbone
            
            # 3. Check third IN predicate with explicit checklistKey -> preserved
            genus_in_pred = predicates[2]
            assert genus_in_pred["type"] == "in"
            assert genus_in_pred["key"] == "GENUS_KEY"
            assert genus_in_pred["values"] == ["5WZMD", "5WZ8T"]
            assert "checklistKey" in genus_in_pred
            assert genus_in_pred["checklistKey"] == "7ddf754f-d193-4cc9-b351-99906754a03b"  # Explicit preserved
            
            # 4. Check non-taxon predicate has NO checklistKey
            country_pred = predicates[3]
            assert country_pred["type"] == "equals"
            assert country_pred["key"] == "COUNTRY"
            assert country_pred["value"] == "US"
            assert "checklistKey" not in country_pred
            
            print(f"✓ IN predicates test passed (alphanumeric → COL XR, numeric → GBIF Backbone, explicit preserved). Download key: {download_key}")
            print(f"  Warning message: {deprecation_warnings[0].message}")

    @vcr.use_cassette("test/vcr_cassettes/test_download_live_simple_in_pred.yaml", filter_headers=["authorization"])
    def test_simple_in_predicate_alphanumeric(self):
        """Test simple 'in' predicate with alphanumeric keys using string syntax"""
        # Simple single IN predicate - alphanumeric keys should get COL XR
        # Note: String values in the array must be quoted for JSON parsing
        query = "taxonKey in ['5WZLF', '623LY', '5WZ4Y']"
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            download_key, payload = occ.download(query)
            
            # Cancel the download immediately
            time.sleep(1)
            occ.download_cancel(download_key)
            
            # Should NOT warn (no numeric keys)
            deprecation_warnings = [warning for warning in w if issubclass(warning.category, DeprecationWarning)]
            assert len(deprecation_warnings) == 0
            
            # Verify the download was created
            assert download_key is not None
            
            # Verify payload includes COL XR at ROOT level
            assert "checklistKey" in payload
            assert payload["checklistKey"] == "7ddf754f-d193-4cc9-b351-99906754a03b"
            
            # Verify the predicate structure (wrapped in AND by default)
            assert "predicate" in payload
            assert payload["predicate"]["type"] == "and"
            assert "predicates" in payload["predicate"]
            assert len(payload["predicate"]["predicates"]) == 1
            
            # Check the IN predicate
            pred = payload["predicate"]["predicates"][0]
            assert pred["type"] == "in"
            assert pred["key"] == "TAXON_KEY"
            assert pred["values"] == ["5WZLF", "623LY", "5WZ4Y"]
            assert "checklistKey" in pred
            assert pred["checklistKey"] == "7ddf754f-d193-4cc9-b351-99906754a03b"  # COL XR
            
            print(f"✓ Simple IN predicate test passed (alphanumeric → COL XR). Download key: {download_key}")

    @vcr.use_cassette("test/vcr_cassettes/test_download_live_simple_in_numeric.yaml", filter_headers=["authorization"])
    def test_simple_in_predicate_numeric(self):
        """Test simple 'in' predicate with numeric keys using dict syntax"""
        # Simple single IN predicate using dict - numeric keys should get GBIF Backbone
        query = {
            "type": "in",
            "key": "SPECIES_KEY",
            "values": ["2435098", "3119195", "212"]
        }
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            download_key, payload = occ.download(query)
            
            # Cancel the download immediately
            time.sleep(1)
            occ.download_cancel(download_key)
            
            # Should warn about numeric keys
            deprecation_warnings = [warning for warning in w if issubclass(warning.category, DeprecationWarning)]
            assert len(deprecation_warnings) == 1
            assert "Numeric taxon keys detected" in str(deprecation_warnings[0].message)
            
            # Verify the download was created
            assert download_key is not None
            
            # Verify payload includes COL XR at ROOT level (always default)
            assert "checklistKey" in payload
            assert payload["checklistKey"] == "7ddf754f-d193-4cc9-b351-99906754a03b"
            
            # Verify the predicate structure (NOT wrapped, dict query stays as-is)
            assert "predicate" in payload
            pred = payload["predicate"]
            assert pred["type"] == "in"
            assert pred["key"] == "SPECIES_KEY"
            assert pred["values"] == ["2435098", "3119195", "212"]
            assert "checklistKey" in pred
            assert pred["checklistKey"] == "d7dddbf4-2cf0-4f39-9b2a-bb099caae36c"  # GBIF Backbone
            
            print(f"✓ Simple IN predicate test passed (numeric → GBIF Backbone). Download key: {download_key}")
            print(f"  Warning message: {deprecation_warnings[0].message}")

    @vcr.use_cassette("test/vcr_cassettes/test_download_live_non_taxon_in.yaml", filter_headers=["authorization"])
    def test_non_taxon_in_predicate(self):
        """Test that non-taxon 'in' predicates do NOT get checklistKey injected"""
        # Non-taxon IN predicates should NOT get checklistKey
        query = {
            "type": "and",
            "predicates": [
                # Non-taxon IN predicates
                {
                    "type": "in",
                    "key": "COUNTRY",
                    "values": ["US", "CA", "MX"]
                },
                {
                    "type": "in",
                    "key": "BASIS_OF_RECORD",
                    "values": ["PRESERVED_SPECIMEN", "OBSERVATION", "HUMAN_OBSERVATION"]
                },
                # Include one taxon predicate for contrast
                {
                    "type": "equals",
                    "key": "TAXON_KEY",
                    "value": "5WZLF"
                }
            ]
        }
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            download_key, payload = occ.download(query)
            
            # Cancel the download immediately
            time.sleep(1)
            occ.download_cancel(download_key)
            
            # Should NOT warn (only alphanumeric taxon key)
            deprecation_warnings = [warning for warning in w if issubclass(warning.category, DeprecationWarning)]
            assert len(deprecation_warnings) == 0
            
            # Verify the download was created
            assert download_key is not None
            
            # Verify payload includes COL XR at ROOT level
            assert "checklistKey" in payload
            assert payload["checklistKey"] == "7ddf754f-d193-4cc9-b351-99906754a03b"
            
            # Verify the predicates structure
            assert "predicate" in payload
            assert "predicates" in payload["predicate"]
            predicates = payload["predicate"]["predicates"]
            assert len(predicates) == 3
            
            # Check COUNTRY IN predicate - should NOT have checklistKey
            country_pred = predicates[0]
            assert country_pred["type"] == "in"
            assert country_pred["key"] == "COUNTRY"
            assert country_pred["values"] == ["US", "CA", "MX"]
            assert "checklistKey" not in country_pred  # Critical assertion
            
            # Check BASIS_OF_RECORD IN predicate - should NOT have checklistKey
            basis_pred = predicates[1]
            assert basis_pred["type"] == "in"
            assert basis_pred["key"] == "BASIS_OF_RECORD"
            assert basis_pred["values"] == ["PRESERVED_SPECIMEN", "OBSERVATION", "HUMAN_OBSERVATION"]
            assert "checklistKey" not in basis_pred  # Critical assertion
            
            # Check TAXON_KEY predicate - SHOULD have checklistKey
            taxon_pred = predicates[2]
            assert taxon_pred["type"] == "equals"
            assert taxon_pred["key"] == "TAXON_KEY"
            assert taxon_pred["value"] == "5WZLF"
            assert "checklistKey" in taxon_pred
            assert taxon_pred["checklistKey"] == "7ddf754f-d193-4cc9-b351-99906754a03b"
            
            print(f"✓ Non-taxon IN predicate test passed (no checklistKey on COUNTRY/BASIS_OF_RECORD). Download key: {download_key}")

    @vcr.use_cassette("test/vcr_cassettes/test_download_live_in_string_syntax.yaml", filter_headers=["authorization"])
    def test_in_string_syntax_with_multiple_keys(self):
        """Test 'in' predicates using string syntax with multiple taxon keys"""
        # Test string syntax parsing for "in" predicates
        # Should detect numeric keys and warn appropriately
        queries = [
            "taxonKey in ['5WZLF', '623LY', '5WZ4Y']",  # Alphanumeric keys -> COL XR
            "speciesKey in [2435098, 3119195]",          # Numeric keys -> GBIF Backbone  
            "country = US"
        ]
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            download_key, payload = occ.download(queries, pred_type="and")
            
            # Cancel the download immediately
            time.sleep(1)
            occ.download_cancel(download_key)
            
            # Should warn about numeric keys
            deprecation_warnings = [warning for warning in w if issubclass(warning.category, DeprecationWarning)]
            assert len(deprecation_warnings) == 1
            assert "Numeric taxon keys detected" in str(deprecation_warnings[0].message)
            
            # Verify the download was created
            assert download_key is not None
            assert len(download_key) > 0
            
            # Verify payload includes COL XR at ROOT level (always default)
            assert "checklistKey" in payload
            assert payload["checklistKey"] == "7ddf754f-d193-4cc9-b351-99906754a03b"
            
            # Verify the predicates structure
            assert "predicate" in payload
            assert "predicates" in payload["predicate"]
            predicates = payload["predicate"]["predicates"]
            assert len(predicates) == 3
            
            # Check first IN predicate with alphanumeric values -> COL XR injected
            taxon_in_pred = predicates[0]
            assert taxon_in_pred["type"] == "in"
            assert taxon_in_pred["key"] == "TAXON_KEY"
            assert taxon_in_pred["values"] == ["5WZLF", "623LY", "5WZ4Y"]
            assert "checklistKey" in taxon_in_pred
            assert taxon_in_pred["checklistKey"] == "7ddf754f-d193-4cc9-b351-99906754a03b"  # COL XR
            
            # Check second IN predicate with numeric values -> GBIF Backbone injected
            species_in_pred = predicates[1]
            assert species_in_pred["type"] == "in"
            assert species_in_pred["key"] == "SPECIES_KEY"
            assert species_in_pred["values"] == [2435098, 3119195]  # Numeric values (no quotes)
            assert "checklistKey" in species_in_pred
            assert species_in_pred["checklistKey"] == "d7dddbf4-2cf0-4f39-9b2a-bb099caae36c"  # GBIF Backbone
            
            # Check non-taxon predicate has NO checklistKey
            country_pred = predicates[2]
            assert country_pred["type"] == "equals"
            assert country_pred["key"] == "COUNTRY"
            assert country_pred["value"] == "US"
            assert "checklistKey" not in country_pred
            
            print(f"✓ IN string syntax test passed (parsed correctly, proper injection). Download key: {download_key}")
            print(f"  Warning message: {deprecation_warnings[0].message}")

    @vcr.use_cassette("test/vcr_cassettes/test_download_live_mixed_in_values.yaml", filter_headers=["authorization"])
    def test_mixed_in_values_default_to_col(self):
        """Test IN predicate with mixed alphanumeric and numeric values defaults to COL XR"""
        # When we have a mix of alphanumeric and numeric values in the same IN predicate,
        # it's ambiguous which checklist to use, so we default to COL XR
        query = {
            "type": "in",
            "key": "TAXON_KEY",
            "values": ["5WZLF", "2435098", "623LY", "3119195"]  # Mixed: 2 alphanumeric, 2 numeric
        }
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            download_key, payload = occ.download(query)
            
            # Cancel immediately
            time.sleep(1)
            occ.download_cancel(download_key)
            
            # Should NOT warn - we're defaulting to COL XR for mixed values
            deprecation_warnings = [warning for warning in w if issubclass(warning.category, DeprecationWarning)]
            assert len(deprecation_warnings) == 0
            
            # Verify download created
            assert download_key is not None
            
            # Verify payload includes COL XR at ROOT level
            assert "checklistKey" in payload
            assert payload["checklistKey"] == "7ddf754f-d193-4cc9-b351-99906754a03b"
            
            # Verify predicate got COL XR (not GBIF Backbone) because values are mixed
            pred = payload["predicate"]
            assert pred["type"] == "in"
            assert pred["key"] == "TAXON_KEY"
            assert pred["values"] == ["5WZLF", "2435098", "623LY", "3119195"]
            assert "checklistKey" in pred
            assert pred["checklistKey"] == "7ddf754f-d193-4cc9-b351-99906754a03b"  # COL XR (not GBIF Backbone)
            
            print(f"✓ Mixed IN values test passed (defaults to COL XR). Download key: {download_key}")

    @vcr.use_cassette("test/vcr_cassettes/test_download_live_not_predicate.yaml", filter_headers=["authorization"])
    def test_not_predicate_with_taxon_key(self):
        """Test that NOT predicates wrapping taxon keys get checklistKey injected correctly"""
        # NOT predicates should recursively process the inner predicate
        query = {
            "type": "and",
            "predicates": [
                # NOT wrapping an alphanumeric taxon key
                {
                    "type": "not",
                    "predicate": {
                        "type": "equals",
                        "key": "TAXON_KEY",
                        "value": "5WZLF"
                    }
                },
                # Regular predicate for contrast
                {
                    "type": "equals",
                    "key": "COUNTRY",
                    "value": "US"
                }
            ]
        }
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            download_key, payload = occ.download(query)
            
            # Cancel immediately
            time.sleep(1)
            occ.download_cancel(download_key)
            
            # Should NOT warn (alphanumeric key)
            deprecation_warnings = [warning for warning in w if issubclass(warning.category, DeprecationWarning)]
            assert len(deprecation_warnings) == 0
            
            # Verify download created
            assert download_key is not None
            
            # Verify payload includes COL XR at ROOT level
            assert "checklistKey" in payload
            assert payload["checklistKey"] == "7ddf754f-d193-4cc9-b351-99906754a03b"
            
            # Verify the NOT predicate structure
            assert "predicate" in payload
            assert "predicates" in payload["predicate"]
            predicates = payload["predicate"]["predicates"]
            assert len(predicates) == 2
            
            # Check NOT predicate
            not_pred = predicates[0]
            assert not_pred["type"] == "not"
            assert "predicate" in not_pred
            
            # Check the inner taxon predicate got checklistKey injected
            inner_pred = not_pred["predicate"]
            assert inner_pred["type"] == "equals"
            assert inner_pred["key"] == "TAXON_KEY"
            assert inner_pred["value"] == "5WZLF"
            assert "checklistKey" in inner_pred
            assert inner_pred["checklistKey"] == "7ddf754f-d193-4cc9-b351-99906754a03b"  # COL XR
            
            # Check COUNTRY predicate has NO checklistKey
            country_pred = predicates[1]
            assert country_pred["type"] == "equals"
            assert country_pred["key"] == "COUNTRY"
            assert country_pred["value"] == "US"
            assert "checklistKey" not in country_pred
            
            print(f"✓ NOT predicate test passed (recursion through NOT works correctly). Download key: {download_key}")

    @vcr.use_cassette("test/vcr_cassettes/test_download_live_all_rank_keys.yaml", filter_headers=["authorization"])
    def test_all_taxonomic_rank_keys(self):
        """Test that all taxonomic rank keys (KINGDOM, PHYLUM, CLASS, ORDER, etc.) get checklistKey injected"""
        # Test various taxonomic rank keys to ensure they all work
        query = {
            "type": "or",
            "predicates": [
                {"type": "equals", "key": "KINGDOM_KEY", "value": "5WZLD"},
                {"type": "equals", "key": "PHYLUM_KEY", "value": "5WZLH"},
                {"type": "equals", "key": "CLASS_KEY", "value": "623M9"},
                {"type": "equals", "key": "ORDER_KEY", "value": "623MD"},
                {"type": "equals", "key": "FAMILY_KEY", "value": "623LY"},
                {"type": "equals", "key": "GENUS_KEY", "value": "5WZ4Y"},
                {"type": "equals", "key": "SPECIES_KEY", "value": "5WZLF"},
                {"type": "equals", "key": "TAXON_KEY", "value": "623M5"},
            ]
        }
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            download_key, payload = occ.download(query)
            
            # Cancel immediately
            time.sleep(1)
            occ.download_cancel(download_key)
            
            # Should NOT warn (all alphanumeric)
            deprecation_warnings = [warning for warning in w if issubclass(warning.category, DeprecationWarning)]
            assert len(deprecation_warnings) == 0
            
            # Verify download created
            assert download_key is not None
            
            # Verify payload includes COL XR at ROOT level
            assert "checklistKey" in payload
            assert payload["checklistKey"] == "7ddf754f-d193-4cc9-b351-99906754a03b"
            
            # Verify all predicates got checklistKey injected
            assert "predicate" in payload
            assert "predicates" in payload["predicate"]
            predicates = payload["predicate"]["predicates"]
            assert len(predicates) == 8
            
            # Check that ALL taxonomic predicates have COL XR checklistKey
            for pred in predicates:
                assert pred["type"] == "equals"
                assert pred["key"] in [
                    "KINGDOM_KEY", "PHYLUM_KEY", "CLASS_KEY", "ORDER_KEY",
                    "FAMILY_KEY", "GENUS_KEY", "SPECIES_KEY", "TAXON_KEY"
                ]
                assert "checklistKey" in pred
                assert pred["checklistKey"] == "7ddf754f-d193-4cc9-b351-99906754a03b"  # All get COL XR
            
            print(f"✓ All rank keys test passed (all taxonomic ranks get checklistKey). Download key: {download_key}")


if __name__ == "__main__":
    """Run live tests manually with: python test/test-occurrences-download_live.py"""
    if SKIP_LIVE_TESTS:
        print(SKIP_REASON)
        print("\nTo run these tests, set environment variables:")
        print("  GBIF_USER=your_username")
        print("  GBIF_PWD=your_password")
        print("  GBIF_EMAIL=your_email@example.com")
    else:
        print("Running live tests with real API requests...")
        print("=" * 70)
        pytest.main([__file__, "-v", "-s"])


