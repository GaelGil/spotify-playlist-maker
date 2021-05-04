import pytest
from twitter import get_search_query, get_uri

def test_get_search_query():
    assert get_search_query('@_gg_bot make this playlist') == ' make this playlist'

def test_get_uri():
    assert get_uri('spotify:playlist:37i9dQZF1DXbYM3nMM0oPk') == '37i9dQZF1DXbYM3nMM0oPk'


