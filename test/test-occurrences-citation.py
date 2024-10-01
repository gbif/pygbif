from pygbif import occurrences
import vcr

@vcr.use_cassette('test/test-occurrences-citation.yaml')
def test_citation():
    res=occurrences.citation("0235283-220831081235567")
    assert "str" == res.__class__.__name__
    "GBIF.org (2 January 2023) GBIF Occurrence Download https://doi.org/10.15468/dl.29wbtx" == res 
