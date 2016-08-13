# ni-recommend
Native Instruments movie recommendation exercise for Python 2.7.

## Install

The following creates a virtualenv `venv` in the project directory and then
installs the dependencies:

    virtualenv venv
    . venv/bin/activate
    pip install .

## Running tests

    cd tests && py.test

## Usage

For usage instructions, see:

    recommend --help

Example usage:

    recommend --limit=10 23 12 10 movies.json

## How it Works

The task is an example of 'Item-based Collaborative Filtering on Unary Data'. In
this.

- Item Similarity - Cosine Similarity
- Normalise (on Unary? check.)
- Compute cosine between two vectors

- Scoring Items

## Future Works
