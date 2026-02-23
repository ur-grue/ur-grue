"""Standalone runner extracted from the Colab notebook bootstrap cell.

This module helps fetch and run the referenced *_run notebook script from a
running Jupyter/Colab session.
"""

from __future__ import annotations

from pathlib import Path
from urllib.parse import unquote

import requests
from notebook import notebookapp  # type: ignore[import-untyped]


class ArtbotRuntimeError(RuntimeError):
    """Raised when the Artbot bootstrap runner cannot discover notebook state."""


def _first_running_server_url() -> str:
    servers = list(notebookapp.list_running_servers())
    if not servers:
        raise ArtbotRuntimeError(
            "No running notebook servers found. Run this inside Colab/Jupyter."
        )
    return str(servers[0]["url"])


def _first_session(server_url: str) -> dict:
    response = requests.get(f"{server_url}api/sessions", timeout=20)
    response.raise_for_status()

    sessions = response.json()
    if not sessions:
        raise ArtbotRuntimeError("No active sessions found on the notebook server.")
    return dict(sessions[0])


def build_download_info() -> tuple[str, str]:
    """Return `(filename, raw_github_url)` for the current notebook session."""
    server_url = _first_running_server_url()
    session = _first_session(server_url)

    name = str(session["name"]).replace("_run", "")
    path_token = str(session["path"]).split("=", 1)[1]

    raw_url = "/".join(unquote(path_token).split("/"))
    raw_url = raw_url.replace("/blob/", "/")
    raw_url = raw_url.replace("github.com", "raw.githubusercontent.com")
    raw_url = raw_url.replace("_run", "")
    return name, raw_url


def download_script(target_dir: Path) -> Path:
    """Download the target script into `target_dir` and return its path."""
    name, raw_url = build_download_info()
    target_dir.mkdir(parents=True, exist_ok=True)
    destination = target_dir / name

    script_response = requests.get(raw_url, timeout=30)
    script_response.raise_for_status()
    destination.write_bytes(script_response.content)
    return destination


def main() -> None:
    destination = download_script(Path("."))
    print(f"Downloaded script to: {destination}")
    print("Execute it manually with: python", destination)


if __name__ == "__main__":
    main()
