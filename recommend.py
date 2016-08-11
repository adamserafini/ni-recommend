import json

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
            }
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
