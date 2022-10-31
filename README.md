# SWAPI Tests

## Description
The Star Wars API tests

## Installation
Prerequisites

```console
Python 3.9 +
```

Clone the repository, make a new virtualenv and install required packages and plugins

```console
1. git clone https://github.com/nbiadrytski/star-wars-api-tests.git
2. cd star-wars-api-tests
3. pip install -r requirements.txt
```

## Usage
How to run tests:

```console
python -m pytest -s --capture=tee-sys --app_host=SWAPI_PROD --may-force=true --html=results/test_report.html -m all
```

where 

`--capture=tee-sys` is a required flag for log output to be populated in html-report. See [bug](https://github.com/pytest-dev/pytest-html/issues/444) for details

`--app_host` environment to run SWAPI tests against (e.g. `SWAPI_PROD`)

`--may-force` outputs additional messages to console if set to True. False by default

`--html` path to a test-report.html file of html-report

`-m` Run a group of tests. E.g. `all` runs all tests, `people` runs `GET /api/people` tests group


## Notes

1. html-report is stored in `results` folder. `Open test_report.html` to view the report 
2. Additional debug-level logs are stored in `results/pytest_debug.log` file
3. See `bug.md` for wookiee format bug report
4. Added console1.png, console2.png and console3.png pictures with console log output
