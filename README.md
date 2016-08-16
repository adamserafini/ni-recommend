# ni-recommend
Native Instruments movie recommendation exercise for Python 2.7 and >=3.2.

## Run Tests

The project uses `tox` to ensure the program runs on multiple versions of
Python. If you do not already have `tox` installed system-wide, install it with
`pip install tox` and then run `tox` from within the project directory.

Tox will run the tests in each of the available Python interpreters on your
system from py27, py32, py33, py34 and py35.

Or, if you just want to run the tests for py27, run:

    tox -e py27

## Install

The following creates a virtualenv `venv` in the project directory:

    virtualenv venv

Or if you want to use Python3:

    virtualenv venv -p python3

Then activate the the virtualenv and install the requirements:

    . venv/bin/activate
    pip install .

## Usage

For usage instructions, see:

    recommend --help

Example usage:

    recommend --limit=10 23 12 10 movies.json

## How it Works

The task is an example of 'Item-based Collaborative Filtering on Unary Ratings'.
Each movie is represented as a binary vector of N dimensions where N is the
number of users. Each element(n) of the movie vector is either 0 or 1 depending
on whether the user(n) has expressed a preference for the movie.

The similarity of any two movies is the "cosine similarity" of their respective
vectors.

The movie IDs passed into the CLI represent the preferences of a hypothetical
user we would like to generate additional recommendations for.

To generate potential recommendations, for any movie(i), its 'score' is the sum
of the cosine similarities between movie(i) and each movie(j) in the query
user's preferences.

The most recommended movies are those with the highest scores: movies with
identical scores are tie-broken by their absolute popularity. This handles the
case where the querying user has no preferences; in this case the most popular
movies are recommended.

## Todo

Here are a few things I would look at if this were real and going into production:

* Better error reporting. For example, at the moment we just tell the user the
  PREFERENCE_DATA is in the wrong schema and don't tell the user how it might
  be fixed.
* Better handling of degenerate cases - in particular the case where no data 
  is available. In that case we should recommend some sensible defaults or
  tell the user there isn't enough data to make recommendations.
* The ItemRecommender is written for simplicity and understanding of the reader,
  not for performance. For example: looping through the user preferences twice
  (once for item popularity, once for similarity). On a dataset of this size,
  it's fine, on a larger data set, it would not be.
* The algorithm matches intuitive expectations for toy examples and makes
  good actual predictions on the given data set (for example, recommending
  the movie Apocalypse Now to fans of A Clockwork Orange). However, a data 
  scientist would probably want to ensure and test that the recommendations 
  are predictive of user preferences on a more rigourous statistical basis.
