import typing
import yaml
from pathlib import Path
from .score import Score


class Scores:
    def __init__(self, max_scores: int, scores: list[Score]) -> None:
        self._max_scores = max_scores
        self._scores = sorted(scores, reverse=True)[:self._max_scores]

    @classmethod
    def default(cls, max_scores: int) -> "Scores":
        return cls(max_scores, [Score(name="Joe", score=100), Score(name="Jack", score=80), Score(name="Averell", score=60), Score(name="William", score=40)])

    def __iter__(self) -> typing.Iterator[Score]:
        return iter(self._scores)



    def is_highscore(self, score_player : int) -> bool :
        """Define the case highscore."""
        return len(self._scores)<self._max_scores or score_player > self._scores[-1].score

    def add_score(self, score_player: Score) -> None:
        """Add a score and sort the list."""
        if self.is_highscore(score_player.score):
            if len(self._scores)>=self._max_scores :
                self._scores.pop()
            self._scores.append(score_player)
            self._scores.sort(reverse=True)

    def save(self, scores_file:Path)->None:
        x=[{"name":s.name, "score": s.score} for s in self]
        with scores_file.open("w") as fd:
            yaml.safe_dump(x, fd)

    @classmethod
    def load(cls, scores_file:Path) -> "Scores":
        with scores_file.open("r") as fd:
            scores = yaml.load(fd, Loader=yaml.Loader)
        return cls(5, [Score(name=c["name"], score=c["score"]) for c in scores])
