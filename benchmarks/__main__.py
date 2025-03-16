from __future__ import annotations

import argparse
import cProfile
import logging
import pstats
import timeit
from typing import TYPE_CHECKING, Any, Optional, Protocol

from .manager import BenchmarkManager

if TYPE_CHECKING:
    from collections.abc import Iterable

    from .manager import BenchmarkCallable


logger = logging.getLogger(__name__)


class _ArgNamespace(Protocol):
    profile: bool
    benchmarks: Optional[list[str]]


def parse_args() -> _ArgNamespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--profile", action="store_true")
    parser.add_argument(
        "-b",
        "--benchmarks",
        nargs="+",
        choices=BenchmarkManager.get_benchmark_names(),
        default=None,
    )

    namespace: _ArgNamespace = parser.parse_args()

    return namespace


def profile(benchmark: BenchmarkCallable[Any], arg: Iterable[Any]) -> None:
    with cProfile.Profile() as pr:
        benchmark(arg)

    ps = pstats.Stats(pr).sort_stats(pstats.SortKey.CUMULATIVE)
    ps.print_stats()


def time(benchmark: BenchmarkCallable[Any], arg: Iterable[Any]) -> None:
    result = timeit.timeit(lambda: benchmark(arg), number=100)
    logger.info("Average runtime after 100 runs: %f s", result / 100)


def main() -> int:
    args = parse_args()

    for benchmark_name, (benchmark, arg) in BenchmarkManager.get_benchmarks(names=args.benchmarks):
        logger.info("Running benchmark: `%s`", benchmark_name)

        if args.profile:
            profile(benchmark, arg)
        else:
            time(benchmark, arg)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
