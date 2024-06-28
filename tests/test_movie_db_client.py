from bechdel_test_predictor.movie_db_client import MovieDbClient


def test_get_movie():
    client = MovieDbClient()
    output = client.get_movie("The Big Short")

    assert output["id"] == 318846
    assert output["title"] == "The Big Short"


def test_get_cast_and_crew():
    client = MovieDbClient()
    id = 318846

    cast = client.get_cast(movie_id=id)
    assert len(cast) == 94

    crew = client.get_crew(movie_id=id)
    assert len(crew) == 205


def test_caching(mocker):
    dummy_credits = {"cast": ["a", "b"], "crew": ["c", "d"]}

    client = MovieDbClient()
    mocker.patch.object(client, "get", return_value=dummy_credits)

    assert client._cache == {}

    _ = client.get_cast(movie_id=12345)
    assert client._cache == {12345: {"credits": dummy_credits}}

    _ = client.get_crew(movie_id=12345)
    assert client.get.call_count == 1
