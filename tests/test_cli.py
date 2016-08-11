import os

import click
from click.testing import CliRunner

from recommend import cli

runner = CliRunner()

def test_no_args():
    result = runner.invoke(cli)
    assert result.exit_code > 0
    assert "Missing argument" in result.output

def test_file_not_exist():
    result = runner.invoke(cli, ['filenotexist'])
    assert result.exit_code > 0
    assert "Could not open file" in result.output

def test_bad_json():
    result = runner.invoke(cli, ['json/bad.json'])
    assert result.exit_code > 0
    assert "not valid JSON" in result.output

def test_no_movies():
    result = runner.invoke(cli, ['json/no_movies.json'])
    assert result.exit_code > 0
    assert "'movies' is a required property" in result.output

def test_no_users():
    result = runner.invoke(cli, ['json/no_users.json'])
    assert result.exit_code > 0
    assert "'users' is a required property" in result.output

def test_bad_movie_id():
    result = runner.invoke(cli, ['json/bad_movie_id.json'])
    assert result.exit_code > 0
    assert "Invalid value" in result.output

def test_empty_movie_title():
    result = runner.invoke(cli, ['json/empty_movie_title.json'])
    assert result.exit_code > 0
    assert "Invalid value" in result.output

def test_no_user_movies():
    result = runner.invoke(cli, ['json/no_user_movies.json'])
    assert result.exit_code > 0
    assert "'movies' is a required property" in result.output

def test_bad_user_movie_id():
    result = runner.invoke(cli, ['json/bad_user_movie_id.json'])
    assert result.exit_code > 0
    assert "not of type 'integer'" in result.output

def test_good_input():
    result = runner.invoke(cli, ['json/good_input.json'])
    assert result.exit_code == 0
