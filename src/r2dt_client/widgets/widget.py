import threading
import time


try:
    from IPython.display import clear_output
    from IPython.display import display
    from ipywidgets import ValueWidget

    _HAS_IPYWIDGETS = True
except ImportError:
    _HAS_IPYWIDGETS = False

from r2dt_client import fetch_results_for
from r2dt_client import submit
from r2dt_client import update_status_for


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
    if not _HAS_IPYWIDGETS:
        print(
            "This function is only available in Jupyter notebooks and "
            "after installing the library with 'pip install "
            "r2dt_client[widgets]'\nConsider using standard API - submit, "
            "update_status_for, fetch_results_for - instead."
        )
        return

    job = submit(sequence)

    spinner = _display_spinner()
    start_time = time.time()

    def job_monitor():
        while not job.done:
            time.sleep(2)
            update_status_for(job)
            elapsed_time = int(time.time() - start_time)
            _update_spinner(spinner, elapsed_time)
        fetch_results_for(job)
        svg_content = job.results["svg"]
        clear_output(wait=True)  # Clear the spinner
        _display_svg(svg_content)

    # Run the monitoring in a separate thread, so it doesn't block the notebook
    thread = threading.Thread(target=job_monitor)
    thread.start()
