# v.1.4.0

## Added

- (#56) Adds ability to execute a job via pynautobot

> Run an instance of the job

```python
# Gets the job from the list of all jobs
>>> gc_backup_job = nautobot.extras.jobs.all()[14]
>>> job_result = gc_backup_job.run()
>>> job_result.result.id
 '1838f8bd-440f-434e-9f29-82b46549a31d' # <-- Job Result ID.
```

> Running the job with inputs

```python
job = nautobot.extras.jobs.all()[7]
job.run(data={"hostname_regex": ".*"})
```

## Updated

- Updates `gitpython` to 3.1.30