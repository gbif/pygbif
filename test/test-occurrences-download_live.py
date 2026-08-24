"""Live tests for occurrences.download with real API requests
These tests make actual requests to the GBIF API and require valid credentials.
They verify the COL Extended Release migration and backward compatibility.

NOTE: These tests are slow (~2-3 seconds per test) due to API rate limits and 
download cancellation delays. GBIF limits users to 3 simultaneous downloads.
"""
import pytest
import os
import warnings
import time
from pygbif import occurrences as occ

# Skip these tests in CI environments - they require real credentials and make real API calls
IN_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"
SKIP_LIVE_TESTS = IN_GITHUB_ACTIONS or not all([
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
        if self.download_keys:
            time.sleep(1)
    
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
        
        # Verify payload includes COL checklistKey
        assert "checklistKey" in payload
        assert payload["checklistKey"] == "7ddf754f-d193-4cc9-b351-99906754a03b"
        
        print(f"✓ COL default test passed. Download key: {download_key}")
    
    def test_numeric_key_automatic_gbif_backbone(self):
        """Test that numeric keys automatically use GBIF Backbone with deprecation warning"""
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
            
            # Verify payload does NOT include checklistKey (uses GBIF Backbone)
            assert "checklistKey" not in payload
            
            print(f"✓ Numeric key test passed. Download key: {download_key}")
            print(f"  Warning message: {w[0].message}")
    
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
    
    def test_explicit_gbif_backbone_no_warning(self):
        """Test that explicitly setting checklistKey=None with numeric keys doesn't warn"""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            # Use numeric key with explicit checklistKey=None
            download_key, payload = occ.download(
                "taxonKey = 2435098",
                checklistKey=None
            )
            self.download_keys.append(download_key)
            
            # Verify NO deprecation warning (user made explicit choice)
            deprecation_warnings = [warn for warn in w if issubclass(warn.category, DeprecationWarning)]
            assert len(deprecation_warnings) == 0
            
            # Verify the download was created
            assert download_key is not None
            assert len(download_key) > 0
            
            # Verify payload does NOT include checklistKey
            assert "checklistKey" not in payload
            
            print(f"✓ Explicit GBIF Backbone test passed. Download key: {download_key}")
    
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
        
        print(f"✓ Mixed predicates test passed. Download key: {download_key}")
    
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
        
        # Verify payload includes COL checklistKey
        assert "checklistKey" in payload
        assert payload["checklistKey"] == "7ddf754f-d193-4cc9-b351-99906754a03b"
        
        print(f"✓ Dict predicate test passed. Download key: {download_key}")
    
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
