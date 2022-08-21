from authorization.utils import score_tweets

def test_score_tweet():
    expected_scores = [
        0.005894356407225132,
        0.9477027654647827
    ]
    tweets = [
        "this is a nice tweet",
        "this is a mean, stupid tweet",
    ]

    actual_scores = score_tweets(tweets)
    assert actual_scores == expected_scores
