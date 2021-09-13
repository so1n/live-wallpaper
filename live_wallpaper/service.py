import datetime
import os
import sys
from typing import Optional

from croniter.croniter import croniter  # type: ignore
from crontab import CronItem, CronTab

from live_wallpaper import wallpaper
from live_wallpaper.config import config, config_filename
from live_wallpaper.lib.current_user import get_current_user


class Service(object):
    cron: CronTab = CronTab(user=get_current_user())

    def __init__(self) -> None:
        self.crontab_comment: str = "live-wallpaper"
        self.crontab_bash: str = "{} {}".format(sys.executable, os.path.realpath(wallpaper.__file__))

    def _search_job(self) -> Optional[CronItem]:
        for job in self.cron:
            if job.comment == self.crontab_comment:
                return job
        return None

    def _status(self, job: Optional[CronItem] = None) -> str:
        job = self._search_job() if job is None else job
        return_str: str = ""
        if job:
            schedule: croniter = job.schedule(date_from=datetime.datetime.now())
            return_str += (
                f"job: {job.comment}\n"
                f"job bash: {job.command}\n"
                f"module: {config.module.module_name} \n"
                f"last run time: {schedule.get_prev()} next run time: {schedule.get_next()}\n"
            )
        else:
            return_str += "The service has stopped, you can start running the service with `start`\n"
        return return_str

    ############
    # user api #
    ############
    def status(self) -> str:
        """View service running status"""
        return_str: str = ""
        return_str += f"user: {get_current_user()}\n"
        return_str += self._status()
        return_str += f"\nlearn more run info from log path: {config_filename}\n"
        return return_str

    def start(self) -> str:
        """start server"""
        job: Optional[CronItem] = self._search_job()
        if job:
            return "The service has been started, you can stop the service with `stop` or view it with `status`"
        else:
            job = self.cron.new(command=self.crontab_bash, comment=self.crontab_comment)
            job.minute.every(15)
            self.cron.write()
            return self._status(job)

    def stop(self) -> str:
        """stop server"""
        job: Optional[CronItem] = self._search_job()
        if job:
            self.cron.remove(job)
            self.cron.write()
            return self._status(job)
        else:
            return "The current task has stopped, you can start running the task with `start`"

    def doctor(self) -> None:
        """Check service running dependencies"""

    def config(self) -> None:
        """view&update config"""
