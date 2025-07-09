from pygbif import occurrences
import vcr

@vcr.use_cassette('test/vcr_cassettes/test-occurrences-download_sql.yaml')
def test_download_sql():
    """basic test of the download_sql function"""
    out = occurrences.download_sql("SELECT gbifid,publishingCountry FROM occurrence WHERE publishingCountry='BE'")
    assert "str" == out.__class__.__name__
    assert 23 == len(out)


