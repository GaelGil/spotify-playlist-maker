import pytest
from twitter import get_search_query, get_uri

def test_get_search_query():
    assert capital_case('@_gg_bot make this playlist') == 'make this playlist'


