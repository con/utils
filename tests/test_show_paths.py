#!/usr/bin/env python3
"""Tests for show-paths utility."""

import os
from pathlib import Path
import re
import subprocess
import sys

import pytest

# Get the path to the bin directory
BIN_DIR = Path(__file__).parent.parent / "bin"
SHOW_PATHS = BIN_DIR / "show-paths"
DATA_DIR = Path(__file__).parent / "data"

# ANSI color codes for verification
ANSI_RED = "\x1b[31m"
ANSI_DARK = "\x1b[2m"
ANSI_RESET = "\x1b[0m"


def run_show_paths(*args, input_data=None, env=None):
    """Helper to run show-paths command."""
    cmd = [sys.executable, str(SHOW_PATHS)] + list(args)
    if env is None:
        env = os.environ.copy()
    result = subprocess.run(
        cmd,
        input=input_data,
        capture_output=True,
        text=True,
        env=env,
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
            line
            for line in lines
            if line.strip().startswith("❯") or "show-paths" in line
        ]
        # If examples are present, there should be some
        if example_lines:
            # Check that example formatting is reasonable
            # (not all squashed into one line)
            assert len(example_lines) > 1, "Examples should span multiple lines"


@pytest.mark.ai_generated
def test_show_paths_help_colors_stripped_without_tty():
    """Test that ANSI color codes are stripped from --help when not a TTY."""
    result = run_show_paths("--help")
    assert result.returncode == 0
    help_output = result.stdout

    # Since we're running in subprocess (no TTY), ANSI codes should be stripped
    assert (
        "\x1b[" not in help_output
    ), "ANSI color codes should be stripped from help without TTY"

    # But the content should still be there
    assert "RepetitionTime" in help_output or "relatedIdentifier" in help_output
    assert "Examples" in help_output


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


@pytest.mark.ai_generated
def test_show_paths_color_on():
    """Test that --color=on adds ANSI color codes to output."""
    # Force termcolor to produce colors even without TTY
    env = os.environ.copy()
    env["FORCE_COLOR"] = "1"

    result = run_show_paths(
        str(DATA_DIR / "sample.py"),
        "-e",
        "find_me",
        "--color",
        "on",
        env=env,
    )
    assert result.returncode == 0
    output = result.stdout

    # Should contain ANSI color codes
    # The matched line should be in red
    assert ANSI_RED in output or "\x1b[" in output, "Color codes should be present"
    # Should contain the matched content
    assert "find_me" in output


@pytest.mark.ai_generated
def test_show_paths_color_on_full_lines():
    """Test that --color=on works with full-lines format."""
    # Force termcolor to produce colors even without TTY
    env = os.environ.copy()
    env["FORCE_COLOR"] = "1"

    result = run_show_paths(
        str(DATA_DIR / "sample.json"),
        "-e",
        "target_field",
        "-f",
        "full-lines",
        "--color",
        "on",
        env=env,
    )
    assert result.returncode == 0
    output = result.stdout

    # Should contain color codes for both path lines (dark) and matched line (red)
    assert "\x1b[" in output, "Color codes should be present in full-lines mode"
    assert "target_field" in output


@pytest.mark.ai_generated
def test_show_paths_color_auto_no_tty():
    """Test that --color=auto produces no colors when not a TTY."""
    # When not connected to a TTY, auto should not produce colors
    result = run_show_paths(
        str(DATA_DIR / "sample.py"),
        "-e",
        "find_me",
        "--color",
        "auto",
    )
    assert result.returncode == 0
    output = result.stdout

    # Since we're running in subprocess (no TTY), should not have color codes
    assert ANSI_RED not in output, "Auto mode should not add colors without TTY"
    assert "find_me" in output


@pytest.mark.ai_generated
def test_show_paths_inline_vs_full_lines_difference():
    """Test that inline and full-lines formats produce different output."""
    inline_result = run_show_paths(
        str(DATA_DIR / "sample.json"),
        "-e",
        "target_field",
        "-f",
        "inline",
        "--color",
        "off",
    )
    full_result = run_show_paths(
        str(DATA_DIR / "sample.json"),
        "-e",
        "target_field",
        "-f",
        "full-lines",
        "--color",
        "off",
    )

    assert inline_result.returncode == 0
    assert full_result.returncode == 0

    inline_output = inline_result.stdout
    full_output = full_result.stdout

    # Both should contain the matched content
    assert "target_field" in inline_output
    assert "target_field" in full_output

    # Full-lines should have more lines (showing the full path)
    inline_lines = len(inline_output.strip().split("\n"))
    full_lines = len(full_output.strip().split("\n"))
    assert full_lines > inline_lines, "Full-lines format should show more lines"

    # Inline should show path in dot notation
    assert ":" in inline_output  # line number:path content
    # Full lines should show actual file lines
    assert "data" in full_output or "{" in full_output


@pytest.mark.ai_generated
def test_show_paths_path_structure():
    """Test that path structure is correctly identified in nested data."""
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

    # Should show a structured path leading to target_field
    # The path should reflect nesting: data -> items -> properties
    lines = output.strip().split("\n")
    assert len(lines) > 0
    # Check that line number is present
    assert any(":" in line for line in lines)


@pytest.mark.ai_generated
def test_show_paths_xml_nested_structure():
    """Test that XML nested structure is correctly parsed."""
    result = run_show_paths(
        str(DATA_DIR / "sample.xml"),
        "-e",
        "target_element",
        "-f",
        "full-lines",
        "--color",
        "off",
    )
    assert result.returncode == 0
    output = result.stdout

    lines = output.strip().split("\n")
    # Should show multiple levels of nesting
    assert len(lines) > 2, "Should show parent elements in the path"

    # Should show the path from root to target
    assert "target_element" in output
    # Check that XML content has indentation (after line number prefix)
    # Lines with increasing indentation indicate nesting
    assert "<content>" in output or "<section" in output
    assert "<subsection>" in output


@pytest.mark.ai_generated
def test_show_paths_python_nested_functions():
    """Test that Python nested function structure is correctly identified."""
    result = run_show_paths(
        str(DATA_DIR / "sample.py"),
        "-e",
        "deeply_nested",
        "-f",
        "full-lines",
        "--color",
        "off",
    )
    assert result.returncode == 0
    output = result.stdout

    lines = output.strip().split("\n")
    # Should show the nesting hierarchy of functions
    assert len(lines) > 1, "Should show parent function definitions"
    assert "deeply_nested" in output


@pytest.mark.ai_generated
def test_show_paths_missing_file():
    """Test behavior when file doesn't exist."""
    result = run_show_paths(
        "/nonexistent/file/path.txt",
        "-e",
        "pattern",
        "--color",
        "off",
    )
    # Should fail with non-zero exit code
    assert result.returncode != 0
    # Should have error message
    assert result.stderr or "No such file" in result.stdout


@pytest.mark.ai_generated
def test_show_paths_empty_file():
    """Test behavior with empty file."""
    empty_file = DATA_DIR / "empty.txt"
    empty_file.write_text("")

    try:
        result = run_show_paths(
            str(empty_file),
            "-e",
            "pattern",
            "--color",
            "off",
        )
        assert result.returncode == 0
        # Empty file with no matches should produce no output
        assert result.stdout.strip() == ""
    finally:
        empty_file.unlink()


@pytest.mark.ai_generated
def test_show_paths_line_number_out_of_range():
    """Test behavior when line number is out of range."""
    result = run_show_paths(
        str(DATA_DIR / "sample.py"),
        "-n",
        "999999",
        "--color",
        "off",
    )
    assert result.returncode == 0
    # Should not crash, just return no results
    assert result.stdout.strip() == ""


@pytest.mark.ai_generated
def test_show_paths_regex_case_sensitive():
    """Test that regex search is case-sensitive by default."""
    # Search for lowercase
    result_lower = run_show_paths(
        str(DATA_DIR / "sample.py"),
        "-e",
        "myclass",
        "--color",
        "off",
    )
    # Search for correct case
    result_correct = run_show_paths(
        str(DATA_DIR / "sample.py"),
        "-e",
        "MyClass",
        "--color",
        "off",
    )

    assert result_lower.returncode == 0
    assert result_correct.returncode == 0

    # Lowercase should find nothing
    assert result_lower.stdout.strip() == ""
    # Correct case should find the class
    assert "MyClass" in result_correct.stdout


@pytest.mark.ai_generated
def test_show_paths_multiple_files():
    """Test show-paths with multiple files."""
    result = run_show_paths(
        str(DATA_DIR / "sample.py"),
        str(DATA_DIR / "sample.json"),
        "-e",
        "target_field",
        "--color",
        "off",
    )
    assert result.returncode == 0
    output = result.stdout
    # Only sample.json has target_field, so output should have its prefix
    assert "sample.json:" in output
    assert "target_field" in output
    # sample.py has no match, so it shouldn't appear
    assert "sample.py:" not in output


@pytest.mark.ai_generated
def test_show_paths_multiple_files_both_match():
    """Test show-paths with multiple files where both have matches."""
    result = run_show_paths(
        str(DATA_DIR / "sample.py"),
        str(DATA_DIR / "sample.xml"),
        "-e",
        "target",
        "--color",
        "off",
    )
    assert result.returncode == 0
    output = result.stdout
    # Both files have "target" somewhere
    assert "sample.py:" in output
    assert "sample.xml:" in output


@pytest.mark.ai_generated
def test_show_paths_multiple_files_auto_prefix():
    """Test that auto mode adds filename prefix for multiple files."""
    result = run_show_paths(
        str(DATA_DIR / "sample.py"),
        str(DATA_DIR / "sample.json"),
        "-e",
        "def",
        "--color",
        "off",
    )
    assert result.returncode == 0
    output = result.stdout
    # Auto mode with multiple files should prefix with filename
    for line in output.strip().split("\n"):
        assert "sample.py:" in line


@pytest.mark.ai_generated
def test_show_paths_single_file_auto_no_prefix():
    """Test that auto mode does NOT add filename prefix for single file."""
    result = run_show_paths(
        str(DATA_DIR / "sample.py"),
        "-e",
        "def",
        "--color",
        "off",
    )
    assert result.returncode == 0
    output = result.stdout
    # Auto mode with single file: no filename prefix
    for line in output.strip().split("\n"):
        assert not line.startswith("sample.py:")


@pytest.mark.ai_generated
def test_show_paths_filename_prefix_single_file():
    """Test --filename=prefix forces prefix even with single file."""
    result = run_show_paths(
        str(DATA_DIR / "sample.py"),
        "-e",
        "find_me",
        "--color",
        "off",
        "--filename",
        "prefix",
    )
    assert result.returncode == 0
    output = result.stdout
    assert "sample.py:" in output
    assert "find_me" in output


@pytest.mark.ai_generated
def test_show_paths_filename_name_mode():
    """Test --filename=name prints filename header before hits."""
    result = run_show_paths(
        str(DATA_DIR / "sample.py"),
        str(DATA_DIR / "sample.json"),
        "-e",
        "target",
        "--color",
        "off",
        "--filename",
        "name",
    )
    assert result.returncode == 0
    output = result.stdout
    lines = output.strip().split("\n")
    # Should have filename as standalone header line
    py_path = str(DATA_DIR / "sample.py")
    json_path = str(DATA_DIR / "sample.json")
    assert py_path in lines
    assert json_path in lines
    # After each header, lines should NOT have filename prefix
    # Find the line after the header
    py_idx = lines.index(py_path)
    assert ":" in lines[py_idx + 1]  # line number format
    assert not lines[py_idx + 1].startswith(py_path + ":")


@pytest.mark.ai_generated
def test_show_paths_filename_name_skips_no_hits():
    """Test --filename=name does not print header for files with no hits."""
    result = run_show_paths(
        str(DATA_DIR / "sample.py"),
        str(DATA_DIR / "sample.json"),
        "-e",
        "target_field",
        "--color",
        "off",
        "--filename",
        "name",
    )
    assert result.returncode == 0
    output = result.stdout
    # Only sample.json has target_field
    assert str(DATA_DIR / "sample.json") in output
    assert str(DATA_DIR / "sample.py") not in output


@pytest.mark.ai_generated
def test_show_paths_multiple_files_full_lines():
    """Test multiple files with full-lines format and prefix."""
    result = run_show_paths(
        str(DATA_DIR / "sample.json"),
        str(DATA_DIR / "sample.xml"),
        "-e",
        "target",
        "-f",
        "full-lines",
        "--color",
        "off",
    )
    assert result.returncode == 0
    output = result.stdout
    # Both context lines and match lines should have the prefix
    json_lines = [
        line
        for line in output.split("\n")
        if line.startswith(str(DATA_DIR / "sample.json:"))
    ]
    xml_lines = [
        line
        for line in output.split("\n")
        if line.startswith(str(DATA_DIR / "sample.xml:"))
    ]
    assert len(json_lines) > 0
    assert len(xml_lines) > 0


# --- Tests for -D/--decorations option ---

FAKE_BLOB_BASE = "https://github.com/owner/repo/blob/abc123"
FAKE_TOPLEVEL = "/fake/repo"
FAKE_SHA = "abc123"


def run_show_paths_with_mock_git(*args, input_data=None):
    """Run show-paths with get_github_context patched to return fake context.

    We read the script, compile it as a module, patch get_github_context,
    then call main().
    """
    show_paths_path = str(SHOW_PATHS)
    wrapper = "\n".join(
        [
            "import sys",
            f"sys.argv = {['show-paths'] + list(args)!r}",
            "import types",
            "mod = types.ModuleType('show_paths')",
            f"mod.__file__ = {show_paths_path!r}",
            f"with open({show_paths_path!r}) as f:",
            f"    code = compile(f.read(), {show_paths_path!r}, 'exec')",
            "exec(code, mod.__dict__)",
            "mod.get_github_context = lambda: "
            f"({FAKE_TOPLEVEL!r}, {FAKE_SHA!r}, {FAKE_BLOB_BASE!r})",
            "mod.main()",
        ]
    )
    cmd = [sys.executable, "-c", wrapper]
    env = os.environ.copy()
    result = subprocess.run(
        cmd,
        input=input_data,
        capture_output=True,
        text=True,
        env=env,
    )
    return result


@pytest.mark.ai_generated
def test_show_paths_decorations_none():
    """Test that --decorations=none produces no ANSI codes."""
    env = os.environ.copy()
    env["FORCE_COLOR"] = "1"
    result = run_show_paths(
        str(DATA_DIR / "sample.py"),
        "-e",
        "find_me",
        "-D",
        "none",
        env=env,
    )
    assert result.returncode == 0
    output = result.stdout
    assert "find_me" in output
    # No ANSI codes should be present
    assert "\x1b[" not in output


@pytest.mark.ai_generated
def test_show_paths_decorations_color():
    """Test that --decorations=color forces ANSI codes even without TTY."""
    env = os.environ.copy()
    env["FORCE_COLOR"] = "1"
    result = run_show_paths(
        str(DATA_DIR / "sample.py"),
        "-e",
        "find_me",
        "-D",
        "color",
        env=env,
    )
    assert result.returncode == 0
    output = result.stdout
    assert "find_me" in output
    assert "\x1b[" in output, "Color codes should be present with --decorations=color"


@pytest.mark.ai_generated
def test_show_paths_github_markdown_inline():
    """Test that github-markdown inline output contains markdown link syntax."""
    result = run_show_paths_with_mock_git(
        str(DATA_DIR / "sample.py"),
        "-e",
        "find_me",
        "-D",
        "github-markdown",
    )
    assert result.returncode == 0
    output = result.stdout
    # Should contain markdown link syntax [...](...#L...)
    assert re.search(
        r"\*\*\[`\d+:`\]\(.+#L\d+\)", output
    ), f"Expected bold markdown link syntax in output: {output}"
    assert FAKE_BLOB_BASE in output
    assert "find_me" in output


@pytest.mark.ai_generated
def test_show_paths_github_markdown_full_lines():
    """Test that github-markdown full-lines output has links for both context and match lines."""
    result = run_show_paths_with_mock_git(
        str(DATA_DIR / "sample.py"),
        "-e",
        "find_me",
        "-f",
        "full-lines",
        "-D",
        "github-markdown",
    )
    assert result.returncode == 0
    output = result.stdout
    lines = output.strip().split("\n")
    # Should have multiple lines (context + match)
    assert len(lines) > 1

    # Context lines should have link syntax with space after number (no colon)
    context_links = [ln for ln in lines if re.search(r"\[`\d+ `\]\(.+#L\d+\)", ln)]
    assert len(context_links) > 0, f"Expected context line links in output: {output}"

    # Match lines should have link syntax with colon after number
    match_links = [ln for ln in lines if re.search(r"\*\*\[`\d+:`\]\(.+#L\d+\)", ln)]
    assert len(match_links) > 0, f"Expected match line links in output: {output}"


@pytest.mark.ai_generated
def test_show_paths_github_markdown_multiple_files():
    """Test that github-markdown produces different blob URLs per file."""
    result = run_show_paths_with_mock_git(
        str(DATA_DIR / "sample.py"),
        str(DATA_DIR / "sample.xml"),
        "-e",
        "target",
        "-D",
        "github-markdown",
    )
    assert result.returncode == 0
    output = result.stdout
    # Both files should have blob URLs with their respective paths
    assert "sample.py" in output
    assert "sample.xml" in output


@pytest.mark.ai_generated
def test_show_paths_github_markdown_line_numbers():
    """Test that GitHub line numbers are 1-indexed (tool's 0-indexed + 1)."""
    result = run_show_paths_with_mock_git(
        str(DATA_DIR / "sample.py"),
        "-n",
        "0",
        "-D",
        "github-markdown",
    )
    assert result.returncode == 0
    output = result.stdout
    # Line 0 in the tool should link to #L1 on GitHub
    assert "#L1)" in output, f"Expected #L1 for line 0 in output: {output}"
    # Should show `0:` as the display number
    assert "`0:`" in output


@pytest.mark.ai_generated
def test_show_paths_decorations_backward_compat():
    """Test that --color off still works when --decorations is not set (auto)."""
    env = os.environ.copy()
    env["FORCE_COLOR"] = "1"
    result = run_show_paths(
        str(DATA_DIR / "sample.py"),
        "-e",
        "find_me",
        "--color",
        "off",
        env=env,
    )
    assert result.returncode == 0
    output = result.stdout
    assert "find_me" in output
    # --color off should suppress colors even with FORCE_COLOR set
    assert "\x1b[" not in output


@pytest.mark.ai_generated
def test_show_paths_github_markdown_filename_prefix_linked():
    """Test that filename prefix in github-markdown mode is a hyperlink."""
    result = run_show_paths_with_mock_git(
        str(DATA_DIR / "sample.py"),
        str(DATA_DIR / "sample.xml"),
        "-e",
        "target",
        "-D",
        "github-markdown",
    )
    assert result.returncode == 0
    output = result.stdout
    # Filename prefix should be a markdown link with backticks
    assert re.search(
        r"\[`[^`]*sample\.py`\]\(" + re.escape(FAKE_BLOB_BASE), output
    ), f"Expected linked filename prefix for sample.py: {output}"


@pytest.mark.ai_generated
def test_show_paths_github_markdown_filename_name_linked():
    """Test that filename header in github-markdown name mode is a hyperlink."""
    result = run_show_paths_with_mock_git(
        str(DATA_DIR / "sample.py"),
        str(DATA_DIR / "sample.xml"),
        "-e",
        "target",
        "--filename",
        "name",
        "-D",
        "github-markdown",
    )
    assert result.returncode == 0
    output = result.stdout
    lines = output.strip().split("\n")
    # Header lines should be linked filenames
    header_lines = [
        ln
        for ln in lines
        if ln.startswith("[`") and "sample.py" in ln and "#L" not in ln
    ]
    assert (
        len(header_lines) > 0
    ), f"Expected linked filename header for sample.py: {output}"
