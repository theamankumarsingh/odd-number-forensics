# Copyright (c) 2026 Aman Kumar Singh
# SPDX-License-Identifier: MIT

import argparse
from odd_number_forensics.io.loader import get_all_experiments, get_experiment
from odd_number_forensics.runner.experiment import run_experiment

def main() -> None:
    parser = argparse.ArgumentParser(description="Run odd-number forensics experiments.")
    parser.add_argument("experiments", nargs="*", help="Experiments to run, relative to the experiments directory.")
    parser.add_argument("--all", action="store_true", help="Run all experiments.")
    parser.add_argument("--stream", action="store_true", help="Stream model thinking and output.")
    args = parser.parse_args()
    if args.all and args.experiments:
        parser.error("--all cannot be used with experiment names.")
    if not args.all and not args.experiments:
        parser.error("Provide at least one experiment or use --all.")
    experiments = get_all_experiments() if args.all else {path: get_experiment(path) for path in args.experiments}
    for path, experiment in experiments.items():
        run_experiment(path, experiment, stream=args.stream)

if __name__ == "__main__":
    main()
