#!/usr/bin/env python3
"""
processor.py - Python processing component
CS 3030 - Project 7: Final Capstone

TODO: Replace this module docstring with a description of what YOUR processor
does, what inputs it accepts, and what outputs it produces.

Example features to implement (replace with your own):
    - Parse or transform input data from a file or stdin
    - Apply analysis, detection, or aggregation logic
    - Write structured output (JSON, CSV, HTML) to a file or stdout
    - Log all operations using the logging module

Usage:
    python3 processor.py --input <path> --output <path> [--format json|csv|text]

Author: Your Name
Date: YYYY-MM-DD
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
# Core processing class
# TODO: Rename this class and update its docstring to match your project.
# ------------------------------------------------------------------------------

class Processor:
    """
    Main processing class.

    TODO: Replace this docstring with a description of what your processor does.

    Attributes:
        input_path (Path): Path to the input file or directory.
        output_path (Path): Path where output will be written.
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
            "processed_at": datetime.now(timezone.utc).isoformat(),
            "input": str(input_path),
            "items_processed": 0,
            "errors": [],
            # TODO: Add fields specific to your project's output.
        }
        logger.info("Processor initialized: input=%s format=%s", input_path, output_format)

    def load_input(self) -> Any:
        """
        Read and return the raw input data.

        TODO: Replace this stub with logic that reads YOUR input format.
              Examples: read a log file line by line, parse a JSON file,
              list files in a directory, call an external API.

        Returns:
            The raw input data in whatever form is useful for process().

        Raises:
            InputError: If the file cannot be read or parsed.
        """
        logger.info("Loading input from: %s", self.input_path)

        # TODO: Replace with your actual input reading logic.
        try:
            # Example: read a plain text file line by line
            lines = self.input_path.read_text(encoding="utf-8").splitlines()
            logger.info("Loaded %d lines from input.", len(lines))
            return lines
        except OSError as exc:
            raise InputError(f"Cannot read input file: {exc}") from exc

    def process(self, data: Any) -> None:
        """
        Apply core logic to the loaded input data and populate self.results.

        TODO: This is where your main logic lives. Replace the example with
              your own implementation — parsing, analysis, detection, etc.

        Args:
            data: The raw input returned by load_input().
        """
        logger.info("Processing %s items...", len(data) if hasattr(data, "__len__") else "?")

        # TODO: Replace this example loop with your actual processing logic.
        for item in data:
            # Example: count non-empty lines
            if item.strip():
                self.results["items_processed"] += 1

            # TODO: Add your analysis here. For example:
            #   - Parse a log line and extract fields
            #   - Check a condition and flag an anomaly
            #   - Aggregate statistics

        logger.info("Processing complete. Items processed: %d", self.results["items_processed"])

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
        description=(
            # TODO: Replace with a one-line description of your tool.
            "Process input data and generate a structured report."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 processor.py --input data/sample.txt --output reports/out.json
  python3 processor.py --input data/ --output reports/out.csv --format csv
  python3 processor.py --input data/sample.txt --output reports/out.txt --format text
        """,
    )

    parser.add_argument(
        "--input", "-i",
        required=True,
        type=Path,
        help="Path to the input file or directory to process.",
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        type=Path,
        help="Path where the output report will be written.",
    )
    parser.add_argument(
        "--format", "-f",
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
