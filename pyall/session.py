from pathlib import Path
from typing import Iterator, List, Tuple

from pyall import utils
from pyall.analyzer import Analyzer
from pyall.config import Config
from pyall.refactor import refactor_source

__all__ = ["Session"]


class Session:
    def __init__(self, config: Config):
        self.config = config

    def get_source(self, path: Path) -> Iterator[Tuple[str, Path]]:
        for py_path in utils.list_paths(
            path, include=self.config.include, exclude=self.config.exclude
        ):
            source, _ = utils.read(py_path)
            yield source, py_path

    @staticmethod
    def get_expected_all(source: str) -> Tuple[bool, List[str]]:
        analyzer = Analyzer(source=source)
        analyzer.traverse()
        action_all = sorted(analyzer.all)
        expected_all = sorted(analyzer.expected_all)
        match = action_all == expected_all
        return match, list(expected_all)

    @classmethod
    def refactor(cls, path: Path, apply: bool = False) -> str:
        source, encoding = utils.read(path)
        _, expected_all = cls.get_expected_all(source)
        new_source = refactor_source(source, expected_all)
        if apply and new_source != source:
            path.write_text(new_source, encoding=encoding)
        return new_source
