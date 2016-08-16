import json

import click
import jsonschema

from src import ItemRecommender

'''
Define a jsonschema representation of the PREFERENCE_DATA to validate against.
It doesn't validate the whole structure: just the data we need in the
required format to make recommendations.
'''
PREFERENCE_DATA_SCHEMA = {
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
          },
        },
        "required": [
          "movies"
        ]
      },
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
    formatted array to STDOUT with its recommendations in descending order
    of confidence.
    """

    # Test the JSON input is valid before proceeding.
    error = ''
    try:
        data = json.load(preference_data)
        jsonschema.validate(data, PREFERENCE_DATA_SCHEMA)
    except ValueError:
        error = "%s is not valid JSON." % preference_data.name
    except jsonschema.ValidationError:
        error = "ensure %s validates against the following JSON schema:\n%s" % \
            (preference_data.name, json.dumps(PREFERENCE_DATA_SCHEMA, indent=1))

    # If the JSON data is invalid, quit and send error to STDERR.
    if error:
        raise click.BadParameter(error, param_hint='PREFERENCE_DATA')

    # Tranform the user input into the format required by ItemRecommender.
    items = {int(key) for key in data['movies']}
    user_prefs = [set(user['movies']) for user in data['users']]
    query = set(movie_ids)

    # Check all movie_ids are present in the PREFERENCE_DATA:
    if not query <= items:
        bad_items = ', '.join([str(i) for i in query - items])
        error = "%s could not be found in PREFERENCE_DATA" % bad_items
        raise click.BadParameter(error, param_hint='MOVIE_IDS')

    recommender = ItemRecommender(items, user_prefs)

    # Query for recommendations, transform to the output format and send to
    # STDOUT.
    top_ids = recommender.recommend(movie_ids, limit)
    results = [{key: data['movies'][str(key)]} for key in top_ids]
    results_formatted = json.dumps(results, indent=1)
    click.echo(results_formatted)
