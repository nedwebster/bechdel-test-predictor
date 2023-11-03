from bechdel_test_predictor import MovieDbClient


def test_get_movie():
    client = MovieDbClient()
    output = client.search_movie("The Big Short")

    assert output["id"] == 318846
    assert output["original_title"] == "The Big Short"
