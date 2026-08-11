#!/usr/bin/env python3
"""
processor.py - Python processing component
CS 3030 - Project 7: Final Capstone

Reads raw metrics (key=value pairs) collected by orchestrator.sh, parses
them into structured data, checks each metric against a defined threshold,
and writes the results to health.json — including a list of any threshold
breaches ("alerts"). This output is what the dashboard (src/dashboard_server.py)
reads and displays.

Usage:
    python3 processor.py --input raw_metrics.txt --output health.json

Author: Jayanti Acharya
Date: 2026-07-27
"""

import argparse
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ------------------------------------------------------------------------------
# Logging setup — structured format with ISO 8601 timestamps
# ------------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%SZ",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


# ------------------------------------------------------------------------------
# Custom exceptions
# ------------------------------------------------------------------------------


class ProcessorError(Exception):
    """Base exception for all processor errors."""


class InputError(ProcessorError):
    """Raised when the input file is missing, unreadable, or malformed."""


class OutputError(ProcessorError):
    """Raised when the output file cannot be written."""


# ------------------------------------------------------------------------------
# Thresholds — tune these against real sample data
# ------------------------------------------------------------------------------
THRESHOLDS = {
    "disk_usage_percent": 85,
    "cpu_load_1min": 4.0,
    "log_size_kb": 500_000,
}


# ------------------------------------------------------------------------------
# Core processing class
# ------------------------------------------------------------------------------


class Processor:
    """
    Aggregates raw system metrics into a health report.

    Parses key=value metric lines produced by orchestrator.sh, checks each
    metric against a threshold, and writes the results — including any
    threshold breaches — to a structured JSON output.

    Attributes:
        input_path (Path): Path to the raw metrics file.
        output_path (Path): Path where health.json will be written.
        output_format (str): Output format — 'json', 'csv', or 'text'.
        results (dict[str, Any]): Accumulated results from processing.
    """

    SUPPORTED_FORMATS = ("json", "csv", "text")

    def __init__(
        self,
        input_path: Path,
        output_path: Path,
        output_format: str = "json",
    ) -> None:
        """
        Initialize the Processor.

        Args:
            input_path: Path to the input file or directory to process.
            output_path: Path where the output report will be written.
            output_format: Desired output format ('json', 'csv', or 'text').

        Raises:
            ValueError: If output_format is not one of the supported formats.
            InputError: If input_path does not exist or is not readable.
        """
        if output_format not in self.SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported format '{output_format}'. "
                f"Choose from: {', '.join(self.SUPPORTED_FORMATS)}"
            )

        if not input_path.exists():
            raise InputError(f"Input path does not exist: {input_path}")

        self.input_path = input_path
        self.output_path = output_path
        self.output_format = output_format
        self.results: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "input": str(input_path),
            "items_processed": 0,
            "errors": [],
            "metrics": {},
            "alerts": [],
        }
        logger.info(
            "Processor initialized: input=%s format=%s", input_path, output_format
        )

    def load_input(self) -> dict[str, Any]:
        """
        Read raw_metrics.txt and parse it into a dict of metric name -> value.

        Each line is expected in key=value format. Values are converted to
        bool, int, or float where possible; malformed lines are skipped with
        a warning rather than crashing the whole run.

        Returns:
            A dict of parsed metrics, e.g. {"disk_usage_percent": 42}.

        Raises:
            InputError: If the file cannot be read.
        """
        logger.info("Loading input from: %s", self.input_path)

        try:
            lines = self.input_path.read_text(encoding="utf-8").splitlines()
        except OSError as exc:
            raise InputError(f"Cannot read input file: {exc}") from exc

        metrics: dict[str, Any] = {}
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if "=" not in line:
                logger.warning("Skipping malformed line: %s", line)
                continue

            key, value = line.split("=", 1)
            metrics[key] = self._convert_value(value)

        logger.info("Loaded %d metrics from input.", len(metrics))
        return metrics

    def _convert_value(self, raw: str) -> Any:
        """Convert a raw string value to bool, int, float, or leave as str."""
        if raw.lower() == "true":
            return True
        if raw.lower() == "false":
            return False
        try:
            return int(raw)
        except ValueError:
            pass
        try:
            return float(raw)
        except ValueError:
            pass
        return raw

    def process(self, data: dict[str, Any]) -> None:
        """
        Check each metric against THRESHOLDS and record any breaches.

        Populates self.results["metrics"] with the parsed data, and
        self.results["alerts"] with a human-readable message for each
        metric that exceeds its threshold.

        Args:
            data: The parsed metrics dict returned by load_input().
        """
        logger.info("Processing %d metrics...", len(data))

        self.results["metrics"] = data
        self.results["items_processed"] = len(data)

        for key, threshold in THRESHOLDS.items():
            if key not in data:
                continue  # metric wasn't collected this run, skip it

            value = data[key]
            if isinstance(value, (int, float)) and value > threshold:
                alert = f"{key} ({value}) exceeded threshold ({threshold})"
                self.results["alerts"].append(alert)
                logger.warning(alert)

        logger.info(
            "Processing complete. %d metrics processed, %d alerts.",
            self.results["items_processed"],
            len(self.results["alerts"]),
        )

    def write_output(self) -> None:
        """
        Write self.results to output_path in the requested format.

        Raises:
            OutputError: If the output file cannot be written.
        """
        logger.info("Writing %s output to: %s", self.output_format, self.output_path)

        try:
            self.output_path.parent.mkdir(parents=True, exist_ok=True)

            if self.output_format == "json":
                self._write_json()
            elif self.output_format == "csv":
                self._write_csv()
            else:
                self._write_text()

        except OSError as exc:
            raise OutputError(f"Cannot write output file: {exc}") from exc

        logger.info("Output written successfully.")

    def _write_json(self) -> None:
        """Write results as a pretty-printed JSON file."""
        # Convert any non-serializable types (e.g., sets, Paths) before dumping.
        serializable = {
            k: list(v) if isinstance(v, set) else str(v) if isinstance(v, Path) else v
            for k, v in self.results.items()
        }
        self.output_path.write_text(
            json.dumps(serializable, indent=2),
            encoding="utf-8",
        )

    def _write_csv(self) -> None:
        """
        Write results as CSV.

        TODO: Adapt the columns and rows to match your results structure.
        """
        import csv  # local import — only needed for this format

        with self.output_path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh)
            writer.writerow(["field", "value"])
            for key, value in self.results.items():
                writer.writerow([key, value])

    def _write_text(self) -> None:
        """
        Write results as a human-readable text report.

        TODO: Customise this to produce the report your project requires.
        """
        lines = [
            "=" * 60,
            "Processing Report",
            f"Generated: {self.results['processed_at']}",
            "=" * 60,
        ]
        for key, value in self.results.items():
            lines.append(f"{key:<25} {value}")
        self.output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def run(self) -> None:
        """
        Execute the full processing pipeline: load → process → write.

        This is the public entry point called from main().
        """
        data = self.load_input()
        self.process(data)
        self.write_output()


# ------------------------------------------------------------------------------
# CLI
# ------------------------------------------------------------------------------


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """
    Parse command-line arguments.

    Args:
        argv: Argument list (defaults to sys.argv[1:] when None).

    Returns:
        Parsed argument namespace.
    """
    parser = argparse.ArgumentParser(
        description="Aggregate raw system metrics into a health report with threshold alerts.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 processor.py --input data/sample.txt --output reports/out.json
  python3 processor.py --input data/ --output reports/out.csv --format csv
  python3 processor.py --input data/sample.txt --output reports/out.txt --format text
        """,
    )

    parser.add_argument(
        "--input",
        "-i",
        required=True,
        type=Path,
        help="Path to the input file or directory to process.",
    )
    parser.add_argument(
        "--output",
        "-o",
        required=True,
        type=Path,
        help="Path where the output report will be written.",
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=Processor.SUPPORTED_FORMATS,
        default="json",
        dest="output_format",
        help="Output format (default: json).",
    )
    # TODO: Add any additional arguments your project needs. Examples:
    #   parser.add_argument("--threshold", type=float, default=0.8)
    #   parser.add_argument("--dry-run", action="store_true")

    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """
    Main entry point.

    Args:
        argv: Optional argument list for testing (defaults to sys.argv[1:]).

    Returns:
        Exit code: 0 on success, 1 on error.
    """
    args = parse_args(argv)

    try:
        processor = Processor(
            input_path=args.input,
            output_path=args.output,
            output_format=args.output_format,
        )
        processor.run()
        logger.info("Done.")
        return 0

    except (ProcessorError, ValueError) as exc:
        logger.error("%s", exc)
        return 1

    except KeyboardInterrupt:
        logger.warning("Interrupted by user.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
