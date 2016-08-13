import py.test

from recommend import cosine_similarity, matrixify, sort_matrix

def test_cosine_similarity():
    assert cosine_similarity([0, 1], [1, 0]) == 0
    assert abs(cosine_similarity([0.5, 1], [1, 0]) - 0.447) < 0.001


def test_matrixify():
    preference_data = {
        "movies": {
            "1": "Toy Story (1994)",
            "2": "GoldenEye (1995)",
            "3": "Twelve Monkeys (1995)"
        },
        "users": [
            {'movies': [2, 3]},
            {'movies': [1, 3]},
            {'movies': [1, 2]},
        ]
    }
    result = matrixify(preference_data)
    assert len(result) == 3
    assert (0, 1, 1) in result and (1, 0, 1) in result and (1, 1, 0) in result

def test_sort_matrix():
    result = sort_matrix(
        (0, 1, 1),
        [(1, 0, 0), (1, 1, 0), (0, 1, 1), (1, 1, 1)]
    )
    assert result == [(0, 1, 1), (1, 1, 1), (1, 1, 0), (1, 0, 0)]
