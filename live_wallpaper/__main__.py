from typer import Typer

from live_wallpaper.service import Service

app: Typer = Typer()
service: Service = Service()


@app.command()
def start_service() -> None:
    """Start service (load bash into crontab file)"""
    service.start()


@app.command()
def service_status() -> None:
    """View the operation details of the service"""
    service.status()


@app.command()
def stop_service() -> None:
    """Stop service (remote bash from crontab file)"""
    service.stop()


@app.command()
def config() -> None:
    """View the service config"""
    service.config()


@app.command()
def doctor() -> None:
    """Check the operating environment status"""
    service.doctor()


if __name__ == "__main__":
    app()
