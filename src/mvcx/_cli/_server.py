import multiprocessing
import os
import shutil
import subprocess
import time
from asyncio import CancelledError
from pathlib import Path

import click

from mvcx._cli._config import BUNDLE_DIR


@click.command()
@click.option("--port", "-p", type=int, default=8000)
@click.option("--fast", "-f", type=bool, is_flag=True)
@click.option("--workers", "-w", type=int)
def start(port: int, fast: bool, workers: int | None) -> None:
    run_cmd = [
        "granian",
        "core.asgi:app",
        "--interface",
        "asgi",
        "--host",
        "0.0.0.0",
        "--port",
        str(port),
    ]

    if fast and workers:
        click.secho(
            "You cannot set both --fast and --workers options.", bold=True, fg="red"
        )
        return

    if fast:
        run_cmd.extend(["--workers", str(multiprocessing.cpu_count())])
    elif workers:
        run_cmd.extend(["--workers", str(workers)])

    process = subprocess.Popen(run_cmd, cwd="src", preexec_fn=os.setsid)
    try:
        process.wait()
    except (KeyboardInterrupt, CancelledError):
        pass
    finally:
        _kill_processes(process)


@click.command()
def dev() -> None:
    bundle_path = Path(BUNDLE_DIR)
    if bundle_path.exists() and bundle_path.is_dir():
        shutil.rmtree(bundle_path)

    processes: list[subprocess.Popen] = []

    try:
        # Bun build
        processes.append(
            subprocess.Popen(
                [
                    "bun",
                    "build",
                    "src/static/index.ts",
                    "--outdir",
                    BUNDLE_DIR,
                    "--watch",
                ],
                preexec_fn=os.setsid,  # Start in a new process group
            )
        )

        # Tailwind
        processes.append(
            subprocess.Popen(
                [
                    "bunx",
                    "@tailwindcss/cli",
                    "-i",
                    "src/static/globals.css",
                    "-o",
                    f"{BUNDLE_DIR}/index.css",
                    "--watch",
                ],
                preexec_fn=os.setsid,
            )
        )

        # Uvicorn
        processes.append(
            subprocess.Popen(
                [
                    "uv",
                    "run",
                    "uvicorn",
                    "core.asgi:app",
                    "--host",
                    "0.0.0.0",
                    "--reload",
                ],
                cwd="src",
                preexec_fn=os.setsid,
            )
        )

        # Browser-sync
        processes.append(
            subprocess.Popen(
                [
                    "bunx",
                    "browser-sync",
                    "http://0.0.0.0:8000",
                    ".",
                    "--watch",
                    "--files",
                    ".",
                    "--no-notify",
                    "--no-open",
                ],
                cwd="src",
                preexec_fn=os.setsid,
            )
        )

        # Wait for all processes to finish (which they won't, until interrupted)
        for p in processes:
            p.wait()

    except (KeyboardInterrupt, CancelledError):
        # We catch both, but the cleanup function is what matters
        pass
    finally:
        _kill_processes(*processes)


def _kill_processes(*processes: subprocess.Popen) -> None:
    for p in processes:
        if p.poll() is None:
            p.terminate()

    time.sleep(2)

    for p in processes:
        if p.poll() is None:
            p.kill()
