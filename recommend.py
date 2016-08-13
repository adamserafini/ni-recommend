import json
import operator
import math

import click
import jsonschema

'''
Define a jsonschema representation of the PREFERENCE_DATA to validate against.
It doesn't validate the whole structure: just the data we need in the
required format to make recommendations.
'''
INPUT_SCHEMA = {
  "properties": {
    "movies": {
      "type": "object",
      "patternProperties": {
        r"^[1-9]\d*$": {
          "type": "string",
          "pattern": r"^.+$"
        }
      },
      "additionalProperties": False
    },
    "users": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "movies": {
            "type": "array",
            "items": {
              "type": "integer"
            },
            "minItems": 1
          },
        },
        "required": [
          "movies"
        ]
      }
    }
  },
  "required": [
    "movies",
    "users"
  ]
}

@click.command()
@click.option('--limit', default=3, type=click.IntRange(min=1),
              help='Limit of recommendations to return (default=3).')
@click.argument('movie_ids', type=click.INT, nargs=-1)
@click.argument('preference_data', type=click.File('rt'), nargs=1)
def cli(limit, movie_ids, preference_data):
    """
    Movie recommender script. The script accepts an unlimited number of movie
    ID numbers and a JSON file of user movie preferences. It returns a JSON
    formatted response to STDOUT with its recommendations.
    """
    try:
        data = json.load(preference_data)
        jsonschema.validate(data, INPUT_SCHEMA)
    except ValueError:
        raise click.BadParameter("%s is not valid JSON." % preference_data.name)
    except jsonschema.ValidationError as e:
        raise click.BadParameter(e.message)

    # Our JSON input has a valid structure but we still need to check the
    # validitiy of the data before computing recommendations.


    # The data is good: we can compute recommendations.
    recommend(movie_ids, preference_data)

# Just pseudo code for now.
def recommend(limit, movie_ids, preference_data):
    # Initialise a list of (score, movies) tuples representing the movies
    # available
    # [(0, {'id': '1'})]
    movie_pool = [(0, {'id': key, 'title': value}) for]

    # movie_ids = [int(key) for key in preference_data['movies']]
    # movie_count = len(movie_ids)


    # Calculate a list of (score, movie) tuples sorted by descending score
    # where a higher score indicates a higher likelihood that a user with
    # preferences = movie_ids will enjoy the movie.
    # movie_scores = sorted(
        [(calculate_movie_score(movie), movie) for movie in movies],
        reverse=True
    )
    # recommendations =  []
    # i = 0
    # while len(recommendations) < limit and i < movie_count:
        if movie not in query:
            recommendations.append

def score_movies(movie_ids, movie_matrix):
    """
    Score movies according to user preference_data and the movie's
    similarity to a query vector (tuple) of movie_ids.

    Args:
        preference_data: A

    Returns:
        A list of tuples:
        [(score, {'id': <id>, 'title': <title>}), ...]
    """
    



def matrixify(preference_data):
    """
    Transform the preference_data into a logical zero/one matrix represented
    as a list of tuples where each tuple represents a user's movie preferences.

    Args:
        preference_data: A dictionary of preference data

    Returns:
        A list of tuples where each tuple represents a user's movie preferences.

    For example, given the following user movie preference_data:

    {
        'movies' ...,
        'users': [
            {'movies': [2, 3], ...},
            {'movies': [1, 3], ...},
            {'movies': [1, 2], ...},
        ]
    }

    Transform into the following matrix:

          Movie1 Movie2 Movie3
    User1   0      1      1
    User2   1      0      1
    User3   1      1      0

    And return the following list of tuples:

    [(0, 1, 1), (1, 0, 1), (1, 1, 0)]
    """
    movies = [
        int(key) for key in preference_data['movies']
    ]
    return [
        tuple(int(movie_id in user['movies']) for movie_id in movies)
        for user in preference_data['users']
    ]

def annotate_matrix(query_vector, matrix):
    """
    Annotate a matrix (list of tuples) with each tuple's similarity score to a
    query vector (tuple)

    Args:
        query_vector: a tuple to compute similarity against.
        matrix: a list of tuples to sort.
    """
    annotated_matrix = [
        (cosine_similarity(query_vector, vector), vector)
        for vector in matrix
    ]
    return [x[1] for x in sorted(annotated_matrix, reverse=True)]

def cosine_similarity(a, b):
    """
    Compute the cosine similarity of two vectors (iterables). Computed as per:
    https://en.wikipedia.org/wiki/Cosine_similarity

    Args:
        a: An iterable of floats.
        b: An iterable of floats.

    Returns:
        Cosine similarity expressed as a float.
    """
    numerator = sum(map(operator.mul, a, b))
    denominator = math.sqrt(sum([x ** 2 for x in a])) * \
                  math.sqrt(sum([x ** 2 for x in b]))

    return numerator / denominator
