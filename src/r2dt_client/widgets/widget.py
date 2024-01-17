import time

from IPython.display import clear_output  # type: ignore
from IPython.display import display  # type: ignore
from ipywidgets import ValueWidget  # type: ignore

from r2dt_client import fetch_results_for
from r2dt_client import submit
from r2dt_client import update_status_for
from r2dt_client.entities import Format


def _display_spinner() -> ValueWidget:
    from ipywidgets import HTML

    spinner = HTML(value="<i>Waiting for results from R2DT...</i>")
    display(spinner)
    return spinner


def _update_spinner(spinner, elapsed_time):
    spinner.value = (
        f"<i>Waiting for results from R2DT... {elapsed_time} seconds elapsed</i>"
    )


def _display_svg(svg_content):
    from IPython.display import HTML

    display(HTML(svg_content))


def draw(sequence: str) -> None:
    job = submit(sequence)

    spinner = _display_spinner()
    start_time = time.time()

    while not job.done:
        time.sleep(2)
        update_status_for(job)
        elapsed_time = int(time.time() - start_time)
        _update_spinner(spinner, elapsed_time)
    fetch_results_for(job)
    svg_content = job.results[Format.svg]
    clear_output(wait=True)  # Clear the spinner
    _display_svg(svg_content)
