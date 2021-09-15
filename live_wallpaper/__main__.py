import pathlib
import sys

import yaml  # type: ignore
from typer import Abort, Option, Typer, colors, confirm, echo, style

from live_wallpaper.config import config as _config
from live_wallpaper.config import config_filename, default_config_filename, reset_config
from live_wallpaper.service import Service, get_current_user

app: Typer = Typer()
service: Service = Service()


@app.command(name="start")
def start_service() -> None:
    """Start service (load bash into crontab file)"""
    # service.start()


@app.command(name="status")
def service_status() -> None:
    """View the operation details of the service"""
    echo(f"User: {style(get_current_user(), fg=colors.GREEN, bold=True)}")
    echo(f"Model: {style(_config.module.module_name, fg=colors.GREEN, bold=True)}")
    echo(f"Python venv: {style(sys.executable, fg=colors.GREEN, bold=True)}")
    status_str, has_job = service.status()
    if not has_job:
        echo(f"Status: {style('Service Fail', fg=colors.RED, bold=True)} ({status_str})")
        echo(style("---------------------------------------", fg=colors.BRIGHT_BLACK, bold=True))
        is_start: bool = confirm("Do you want to start?")
        if is_start:
            start_service()


@app.command(name="stop")
def stop_service() -> None:
    """Stop service (remote bash from crontab file)"""
    # service.stop()


@app.command(name="config", no_args_is_help=True)
def config(
    output_format: str = Option(default="", show_default=False, help="output config format, only support json or yaml"),
    reset: bool = Option(default=False, show_default=False, help="reset or create default config to default config"),
    reset_from_filename: str = Option(
        default=False,
        show_default=False,
        exists=True,
        help=f"reset config from specify filename, e.g default config filename:{default_config_filename}",
    ),
) -> None:
    """View the service config"""
    config_exists: bool = pathlib.Path(config_filename).exists()
    if config_exists:
        echo(f"config file path:{style(config_filename, fg=colors.GREEN, bold=True)}")
    else:
        echo(style(f"Can not found config:{config_filename}", fg=colors.RED, bold=True))
    if output_format:
        if not config_exists:
            return
        echo()
        if output_format == "json":
            echo(_config.model.json(indent=2))
        elif output_format == "yaml":
            echo(yaml.dump(_config.model.dict()))
        else:
            Abort(f"output not support {output_format}")
    elif reset:
        if config_exists:
            msg: str = "Do you want to reset config?"
        else:
            msg = "Do you want to create default config?"
        is_reset: bool = confirm(msg)
        if is_reset:
            reset_config()
        else:
            Abort("Cancel reset config")

    elif reset_from_filename:
        if not pathlib.Path(reset_from_filename).exists():
            echo(f"{reset_from_filename} not exists")
            return
        if config_exists:
            msg = f"Do you want to reset config from:{reset_from_filename}?"
        else:
            msg = "Do you want to create default config?"
        is_reset = confirm(msg)
        if is_reset:
            reset_config()
        else:
            Abort("Cancel reset config from filename")


@app.command()
def doctor() -> None:
    """Check the operating environment status"""
    echo(_config.module.json())


if __name__ == "__main__":
    app()
