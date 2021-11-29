from async.Job import Job
from core.scheduler.Scheduler import schedule_function


class AsyncScheduler:

    @staticmethod
    def schedule_job(job: Job):
        # hack for args always being an object when passed as argument
        schedule_function(job.func, job.args, delay=job.delay)

    @staticmethod
    def schedule_jobs(*jobs: Job):
        for job in jobs:
            AsyncScheduler.schedule_job(job)
