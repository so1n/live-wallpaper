import argparse
import datetime
import os
import sys
from typing import Any, Optional

from croniter.croniter import croniter  # type: ignore
from crontab import CronItem, CronTab

from live_wallpaper import wallpaper
from live_wallpaper.config import config, config_filename
from live_wallpaper.lib.current_user import get_current_user


class Service(object):
    cron: CronTab = CronTab(user=get_current_user())

    def __init__(self) -> None:
        self.crontab_comment: str = config.system.crontab_comment
        self.crontab_bash: str = "{} {}".format(sys.executable, os.path.realpath(wallpaper.__file__))

    def _search_job(self) -> Optional[CronItem]:
        for job in self.cron:
            if job.comment == self.crontab_comment:
                return job
        return None

    def _status(self, job: Optional[CronItem] = None) -> None:
        job = self._search_job() if job is None else job
        if job:
            schedule: croniter = job.schedule(date_from=datetime.datetime.now())
            self.output(f"job: {job.comment}")
            self.output(f"job bash: {job.command}")
            self.output(f"last run time: {schedule.get_prev()} next run time: {schedule.get_next()}")
        else:
            self.output("The service has stopped, you can start running the service with `start`")

    def output(self, msg: str) -> None:
        print(msg)

    ############
    # user api #
    ############
    def status(self) -> None:
        """View service running status"""
        self.output(f"user: {get_current_user()}")
        self._status()
        self.output(f"\nlearn more run info from log path: {config_filename}")

    def start(self) -> None:
        """start server"""
        job: Optional[CronItem] = self._search_job()
        if job:
            self.output("The service has been started, you can stop the service with `stop` or view it with `status`")
        else:
            job = self.cron.new(command=self.crontab_bash, comment=self.crontab_comment)
            job.minute.every(15)
            self.cron.write()
            self._status(job)

    def stop(self) -> None:
        """stop server"""
        job: Optional[CronItem] = self._search_job()
        if job:
            self.cron.remove(job)
            self.cron.write()
            self._status(job)
        else:
            self.output("The current task has stopped, you can start running the task with `start`")

    def doctor(self) -> None:
        """Check service running dependencies"""

    def config(self) -> None:
        """view&update config"""


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument(dest="method", metavar="method", nargs="*", help="lalala")

    args: Any = parser.parse_args()
    service: Service = Service()

    try:
        method = args.method[0]
        if method == "start":
            service.start()
        elif method == "status":
            service.status()
        elif method == "stop":
            service.stop()
        else:
            service.output("use -h to show help message and exit")
    except IndexError:
        service.output("use -h to show help message and exit")
