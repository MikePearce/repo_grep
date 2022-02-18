# repo_grep

Want to know which are your most stale, smelly and out of date repos? Then wonder no more! Repo_grep has got your back.

Simply generate your github token, point it at your org and hooray!

## Installation

`pip install PyGithub python-dateutil tabulate`

## Usage

```
usage: main.py [-h] [-o ORG] [-t TOKEN] [-d DURATION] [-dt DURATION_TYPE]

optional arguments:
  -h, --help            show this help message and exit
  -o ORG, --organisation ORG
                        Provide GitHub org name. Defaults to none.
  -t TOKEN, --token TOKEN
                        Provide a GitHub token. Defaults to none.
  -d DURATION, --duration DURATION
                        The number of minutes/weeks/months/years. Defaults to 6.
  -dt DURATION_TYPE, --durationtype DURATION_TYPE
                        The type of duration: minutes|days|weeks|months|years. Defaults to months.
```
