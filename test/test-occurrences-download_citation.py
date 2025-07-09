from pygbif import occurrences as occ
import vcr

@vcr.use_cassette('test/vcr_cassettes/test-occurrences-download_citation.yaml')
def test_download_citation():
    res=occ.download_citation("0235283-220831081235567")
    assert "str" == res.__class__.__name__
    "GBIF.org (2 January 2023) GBIF Occurrence Download https://doi.org/10.15468/dl.29wbtx" == res 

def test_download_citation_failswell():
    try:
        occ.download_citation("dog")
    except ValueError as e:
        assert str(e) == "key must be a GBIF download key"

