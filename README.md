# R2DT API Client

[![PyPI](https://img.shields.io/pypi/v/r2dt-client.svg)][pypi_]
[![Status](https://img.shields.io/pypi/status/r2dt-client.svg)][status]
![Static Badge](https://img.shields.io/badge/Python_version-3.9%2B-blue)

[![License](https://img.shields.io/pypi/l/r2dt-client)][license]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi_]: https://pypi.org/project/r2dt-client/
[CI]: https://github.com/anayden/r2dt-client/actions

## Features

- Access to the [R2DT] API via Python
- Display R2DT widget in Jupyter Notebook

## Requirements

- Python 3.9+
- [pdm] 2.0.0+

## Installation

You can install _R2DT API Client_ via [pip] from [PyPI]:

```console
$ pip install r2dt-client
```

## Usage

Example usage in the code:

```python
from time import sleep
from r2dt_client import setup, submit, update_status_for, fetch_results_for

setup(email="YOUR_EMAIL")

job = submit(
    ">S box leader))\nCTCTTATCGAGAGTTGGGCGAGGGATTTGGCCTTTTGACCCCAAAAGCAACCGACCGTAATTCCATTGTGAAATGGGGCGCATTTTTTTCGCGCCGAGACGCTGGTCTCTTAAGGCACGGTGCTAATTCCATTCAGATCTGATCTGAGAGATAAGAG")
while not job.done:
    update_status_for(job)
    sleep(5)

fetch_results_for(job)
print(job.results['fasta'])
```

Using the widget via Jupyter Notebook:

```jupyter
!pip install r2dt_client

from r2dt_client import setup, draw

setup(email="YOUR_EMAIL")
draw(
    ">S box leader))\nCTCTTATCGAGAGTTGGGCGAGGGATTTGGCCTTTTGACCCCAAAAGCAACCGACCGTAATTCCATTGTGAAATGGGGCGCATTTTTTTCGCGCCGAGACGCTGGTCTCTTAAGGCACGGTGCTAATTCCATTCAGATCTGATCTGAGAGATAAGAG")
```

## License

Distributed under the terms of the [MIT license][license],
_R2DT API Client_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.