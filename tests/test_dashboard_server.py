"""
test_dashboard_server.py - pytest suite for the Infrastructure Health Dashboard
CS 3030 - Project 7: Final Capstone
Owner: Omar

Tests the dashboard's JSON loading, HTML rendering, error handling,
and an actual HTTP request against the dashboard server.
"""

import json
import threading
import urllib.request
import urllib.error
import pytest
from http.server import HTTPServer

from dashboard_server import DashboardHandler, load_health_data, render_html


def sample_health_data():
    """Return representative health data matching processor.py output."""
    return {
        "timestamp": "2026-08-12T09:05:48+00:00",
        "input": "raw_metrics.txt",
        "items_processed": 6,
        "errors": [],
        "metrics": {
            "disk_usage_percent": 25,
            "cpu_load_1min": 0.76,
            "process_count": 180,
            "log_size_kb": 0,
            "docker_available": True,
            "docker_container_count": 1,
        },
        "alerts": [],
    }


def test_load_health_data_reads_valid_json(tmp_path):
    """A valid health.json file should be loaded into a dictionary."""
    health_file = tmp_path / "health.json"
    expected = sample_health_data()

    health_file.write_text(json.dumps(expected), encoding="utf-8")

    result = load_health_data(health_file)

    assert result == expected
    assert result["metrics"]["disk_usage_percent"] == 25


def test_load_health_data_handles_missing_file(tmp_path):
    """A missing health file should return an error instead of crashing."""
    missing_file = tmp_path / "missing.json"

    result = load_health_data(missing_file)

    assert result["metrics"] == {}
    assert result["alerts"] == []
    assert result["errors"]
    assert "not found" in result["errors"][0].lower()


def test_load_health_data_handles_invalid_json(tmp_path):
    """Malformed JSON should return a useful error dictionary."""
    health_file = tmp_path / "health.json"
    health_file.write_text("{invalid json", encoding="utf-8")

    result = load_health_data(health_file)

    assert result["metrics"] == {}
    assert result["errors"]
    assert "invalid health report json" in result["errors"][0].lower()


def test_render_html_shows_healthy_status():
    """A report without alerts or errors should display HEALTHY."""
    page = render_html(sample_health_data())

    assert "Overall Status: HEALTHY" in page
    assert "Infrastructure Health Dashboard" in page


def test_render_html_displays_metrics():
    """Processor-generated metric names and values should appear in the page."""
    page = render_html(sample_health_data())

    assert "Disk Usage Percent" in page
    assert ">25<" in page
    assert "Cpu Load 1Min" in page
    assert ">0.76<" in page
    assert "Docker Container Count" in page


def test_render_html_shows_warning_when_alert_exists():
    """A threshold alert should change the dashboard status to WARNING."""
    data = sample_health_data()
    data["alerts"] = ["disk_usage_percent (92) exceeded threshold (85)"]

    page = render_html(data)

    assert "Overall Status: WARNING" in page
    assert "disk_usage_percent (92) exceeded threshold (85)" in page


def test_http_server_serves_health_json(tmp_path):
    """
    Integration test: start the real HTTP handler and request /health.json.

    This verifies that the HTTP server can read a processor-compatible JSON
    file and return it through the dashboard endpoint.
    """
    health_file = tmp_path / "health.json"
    expected = sample_health_data()
    health_file.write_text(json.dumps(expected), encoding="utf-8")

    DashboardHandler.health_file = health_file

    # Port 0 asks the operating system to choose an available temporary port.
    server = HTTPServer(("127.0.0.1", 0), DashboardHandler)
    port = server.server_address[1]

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        with urllib.request.urlopen(
            f"http://127.0.0.1:{port}/health.json",
            timeout=5,
        ) as response:
            returned_data = json.loads(response.read().decode("utf-8"))

        assert response.status == 200
        assert returned_data["metrics"]["process_count"] == 180
        assert returned_data["items_processed"] == 6

    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_load_health_data_handles_os_error(tmp_path):
    """An operating-system read error should be reported without crashing."""
    # Passing a directory instead of a JSON file causes Path.read_text()
    # to raise an OSError-derived exception such as IsADirectoryError.
    result = load_health_data(tmp_path)

    assert result["metrics"] == {}
    assert result["alerts"] == []
    assert result["errors"]
    assert "unable to read health report" in result["errors"][0].lower()


def test_render_html_handles_invalid_field_types():
    """
    Unexpected field types should be normalized into a safe error dashboard.

    This verifies that malformed processor data cannot crash HTML rendering.
    """
    data = {
        "timestamp": "2026-08-12T09:05:48+00:00",
        "metrics": "not-a-dictionary",
        "alerts": "single alert",
        "errors": "single error",
    }

    page = render_html(data)

    assert "Overall Status: ERROR" in page
    assert "No metrics are currently available." in page
    assert "single alert" in page
    assert "single error" in page


def test_http_server_serves_html_head_and_404(tmp_path):
    """
    Integration test for dashboard HTML, HEAD requests, and invalid routes.

    A real temporary HTTP server is started so the handler is exercised the
    same way it is when running locally or inside Docker.
    """
    health_file = tmp_path / "health.json"
    health_file.write_text(
        json.dumps(sample_health_data()),
        encoding="utf-8",
    )

    DashboardHandler.health_file = health_file

    server = HTTPServer(("127.0.0.1", 0), DashboardHandler)
    port = server.server_address[1]

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        # Verify the main HTML dashboard route.
        with urllib.request.urlopen(
            f"http://127.0.0.1:{port}/",
            timeout=5,
        ) as response:
            page = response.read().decode("utf-8")

        assert response.status == 200
        assert "Overall Status: HEALTHY" in page
        assert "Infrastructure Health Dashboard" in page

        # Verify HEAD support for the generated JSON endpoint.
        json_head_request = urllib.request.Request(
            f"http://127.0.0.1:{port}/health.json",
            method="HEAD",
        )

        with urllib.request.urlopen(
            json_head_request,
            timeout=5,
        ) as response:
            assert response.status == 200
            assert response.headers["Content-Type"].startswith("application/json")
            assert response.read() == b""

        # Verify HEAD support for the HTML dashboard.
        html_head_request = urllib.request.Request(
            f"http://127.0.0.1:{port}/",
            method="HEAD",
        )

        with urllib.request.urlopen(
            html_head_request,
            timeout=5,
        ) as response:
            assert response.status == 200
            assert response.headers["Content-Type"].startswith("text/html")
            assert response.read() == b""

        # Verify an unsupported path returns HTTP 404.
        with pytest.raises(urllib.error.HTTPError) as error:
            urllib.request.urlopen(
                f"http://127.0.0.1:{port}/does-not-exist",
                timeout=5,
            )

        assert error.value.code == 404

    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
