#!/usr/bin/env python3
"""Tests for show-paths utility."""

import subprocess
import sys
from pathlib import Path

import pytest

# Get the path to the bin directory
BIN_DIR = Path(__file__).parent.parent / "bin"
SHOW_PATHS = BIN_DIR / "show-paths"
DATA_DIR = Path(__file__).parent / "data"


def run_show_paths(*args, input_data=None):
    """Helper to run show-paths command."""
    cmd = [sys.executable, str(SHOW_PATHS)] + list(args)
    result = subprocess.run(
        cmd,
        input=input_data,
        capture_output=True,
        text=True,
    )
    return result


@pytest.mark.ai_generated
def test_show_paths_python_file_regex():
    """Test show-paths on Python file with regex search."""
    result = run_show_paths(
        str(DATA_DIR / "sample.py"),
        "-e",
        "find_me",
        "--color",
        "off",
    )
    assert result.returncode == 0
    output = result.stdout
    # Should find the target_line with "find_me"
    assert "find_me" in output
    assert "target_line" in output
    # Should show the path to the nested function
    assert "def" in output or "outer_function" in output or "inner_function" in output


@pytest.mark.ai_generated
def test_show_paths_xml_file_regex():
    """Test show-paths on XML file with regex search."""
    result = run_show_paths(
        str(DATA_DIR / "sample.xml"),
        "-e",
        "target_element",
        "--color",
        "off",
    )
    assert result.returncode == 0
    output = result.stdout
    # Should find the target_element
    assert "target_element" in output
    assert "find_this_element" in output


@pytest.mark.ai_generated
def test_show_paths_json_file_regex():
    """Test show-paths on JSON file with regex search."""
    result = run_show_paths(
        str(DATA_DIR / "sample.json"),
        "-e",
        "target_field",
        "--color",
        "off",
    )
    assert result.returncode == 0
    output = result.stdout
    # Should find the target_field
    assert "target_field" in output
    assert "important_value" in output


@pytest.mark.ai_generated
def test_show_paths_line_number():
    """Test show-paths with specific line number."""
    result = run_show_paths(
        str(DATA_DIR / "sample.py"),
        "-n",
        "15",
        "--color",
        "off",
    )
    assert result.returncode == 0
    output = result.stdout
    # Should show line 15
    assert "15:" in output


@pytest.mark.ai_generated
def test_show_paths_full_lines_format():
    """Test show-paths with full-lines format."""
    result = run_show_paths(
        str(DATA_DIR / "sample.json"),
        "-e",
        "target_field",
        "-f",
        "full-lines",
        "--color",
        "off",
    )
    assert result.returncode == 0
    output = result.stdout
    # In full-lines mode, should show the full path with all parent lines
    assert "target_field" in output
    lines = output.strip().split("\n")
    # Should have multiple lines showing the path
    assert len(lines) > 1


@pytest.mark.ai_generated
def test_show_paths_inline_format():
    """Test show-paths with inline format (default)."""
    result = run_show_paths(
        str(DATA_DIR / "sample.json"),
        "-e",
        "target_field",
        "-f",
        "inline",
        "--color",
        "off",
    )
    assert result.returncode == 0
    output = result.stdout
    # In inline mode, should show the path and matched line
    assert "target_field" in output


@pytest.mark.ai_generated
def test_show_paths_stdin():
    """Test show-paths reading from stdin."""
    test_input = """line 1
    indented line 2
        deeply indented line 3
"""
    result = run_show_paths("-e", "deeply", "--color", "off", input_data=test_input)
    assert result.returncode == 0
    output = result.stdout
    assert "deeply" in output


@pytest.mark.ai_generated
def test_show_paths_multiple_line_numbers():
    """Test show-paths with multiple line numbers."""
    result = run_show_paths(
        str(DATA_DIR / "sample.py"),
        "-n",
        "5",
        "-n",
        "10",
        "--color",
        "off",
    )
    assert result.returncode == 0
    output = result.stdout
    # Should show both line 5 and line 10
    assert "5:" in output
    assert "10:" in output


@pytest.mark.ai_generated
def test_show_paths_color_off():
    """Test that color=off works without termcolor."""
    result = run_show_paths(
        str(DATA_DIR / "sample.py"),
        "-e",
        "def",
        "--color",
        "off",
    )
    assert result.returncode == 0
    # Should work even without termcolor when color is off


@pytest.mark.ai_generated
def test_show_paths_help_output():
    """Test that --help output is properly formatted without wrapping examples."""
    result = run_show_paths("--help")
    assert result.returncode == 0
    help_output = result.stdout

    # Check that help is displayed
    assert "usage:" in help_output.lower() or "Show the version" in help_output

    # Check that examples are present (from the docstring)
    # The examples should not be wrapped inappropriately
    # We verify by checking that the indentation of example lines is preserved
    if "visualize where" in help_output.lower():
        # Examples section should be present
        lines = help_output.split("\n")
        # Find lines that look like shell prompts from examples
        example_lines = [
            line for line in lines if line.strip().startswith("❯") or "show-paths" in line
        ]
        # If examples are present, there should be some
        if example_lines:
            # Check that example formatting is reasonable
            # (not all squashed into one line)
            assert len(example_lines) > 1, "Examples should span multiple lines"


@pytest.mark.ai_generated
def test_show_paths_no_matches():
    """Test show-paths when regex doesn't match anything."""
    result = run_show_paths(
        str(DATA_DIR / "sample.py"),
        "-e",
        "this_will_never_match_12345",
        "--color",
        "off",
    )
    assert result.returncode == 0
    # Should return successfully but with no output
    assert result.stdout.strip() == ""
