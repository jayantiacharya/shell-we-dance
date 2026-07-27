"""
test_processor.py - pytest suite for the aggregator
CS 3030 - Project 7: Final Capstone
Owner: Jayanti
"""

from pathlib import Path
import pytest
from processor import Processor, InputError

FIXTURES = Path(__file__).parent / "fixtures"


def test_load_input_parses_valid_metrics():
    p = Processor(
        input_path=FIXTURES / "sample_metrics.txt",
        output_path=Path("/tmp/health.json"),
    )
    metrics = p.load_input()

    assert metrics["disk_usage_percent"] == 92
    assert metrics["cpu_load_1min"] == 0.35
    assert metrics["docker_available"] is True


def test_load_input_skips_malformed_lines(tmp_path):
    bad_file = tmp_path / "bad_metrics.txt"
    bad_file.write_text("disk_usage_percent=42\nnotvalidline\n\ncpu_load_1min=0.1\n")

    p = Processor(input_path=bad_file, output_path=tmp_path / "out.json")
    metrics = p.load_input()

    assert metrics == {"disk_usage_percent": 42, "cpu_load_1min": 0.1}


def test_load_input_raises_on_missing_file(tmp_path):
    missing = tmp_path / "does_not_exist.txt"
    with pytest.raises(InputError):
        Processor(input_path=missing, output_path=tmp_path / "out.json")


def test_process_flags_threshold_breach():
    p = Processor(
        input_path=FIXTURES / "sample_metrics.txt",
        output_path=Path("/tmp/health.json"),
    )
    data = p.load_input()
    p.process(data)

    assert len(p.results["alerts"]) == 1
    assert "disk_usage_percent" in p.results["alerts"][0]


def test_process_no_alert_when_under_threshold(tmp_path):
    good_file = tmp_path / "good_metrics.txt"
    good_file.write_text("disk_usage_percent=10\ncpu_load_1min=0.1\n")

    p = Processor(input_path=good_file, output_path=tmp_path / "out.json")
    data = p.load_input()
    p.process(data)

    assert p.results["alerts"] == []
