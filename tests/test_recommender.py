import py.test
import math

from src import ItemRecommender

def test_cosine_similarity():
    r = ItemRecommender({1, 2, 3, 4}, [{1, 2}, {2, 3}])
    assert r.similarity(1, 2) == 1 / (math.sqrt(1) * math.sqrt(2))
    assert r.similarity(1, 0) == 0.0

def test_popularity():
    r = ItemRecommender({1, 2, 3, 4}, [{1, 2, 3}, {1, 2}, {1}])
    assert r.popularity(4) == 0
    assert r.popularity(3) == 1
    assert r.popularity(2) == 2
    assert r.popularity(1) == 3

def test_rankings():
    # Check some toy examples match with intuition.
    r = ItemRecommender({1, 2, 3, 4, 5, 6},
        [{1, 2, 3}, {1, 2, 3}, {1, 2, 4}, {1, 5}])
    assert r.recommend({1, 2}, limit=3) == [3, 4, 5]

    r.user_prefs = [{1, 2, 3}, {1, 2, 3}, {1, 2, 4}, {1, 2, 5}, {5, 6}]
    assert r.recommend({1, 2}, limit=4) == [3, 4, 5, 6]

def test_popularity_tie_breaking():
    r = ItemRecommender({1, 2, 3, 4}, [{1, 2}, {3, 4}, {3}])
    assert r.recommend({1}, limit=3) == [2, 3, 4]
    assert r.recommend({}, limit=1) == [3]
