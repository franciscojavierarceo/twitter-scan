from authorization.utils import score_tweets, batch_score
from typing import List

def _rounds(x: List[float], val: int=6):
    return [round(s, val) for s in x]

class TestScoring:
    # note that we are rounding here because after about 7 digits I got
    # different estimates from my linux computer vs my mac...probably a
    # reason for it but won't investigate now
    expected_scores = [
        0.005894,
        0.947703,
    ]
    tweets = [
        "this is a nice tweet",
        "this is a mean, stupid tweet",
    ]


    def test_score_tweet(self):
        actual_scores = _rounds(score_tweets(self.tweets))
        assert actual_scores == self.expected_scores


    def test_batch_scoring(self):
        tweets = self.tweets * 3
        expected_scores = self.expected_scores * 3
        actual_scores = _rounds(batch_score(tweets, batch_size=2))
        assert actual_scores == expected_scores

