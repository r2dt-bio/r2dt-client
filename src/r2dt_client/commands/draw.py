import asyncio
from time import time

from IPython import get_ipython  # type: ignore
from IPython.display import SVG
from IPython.display import clear_output
from IPython.display import display

from r2dt_client.session.entities.format import Format
from r2dt_client.session.session import R2dtClient


__all__ = ["draw_rna"]


async def draw_rna(email: str, sequence: str) -> None:
    try:
        # This will only succeed in a Jupyter or Colab environment
        ipython_result = str(get_ipython())  # type: ignore
        # If in Google Colab, import the required module
        if "google.colab" in ipython_result:
            from google.colab import output  # type: ignore

            output.enable_custom_widget_manager()
    except NameError:
        print(
            "SVG drawing is only supported within a Jupyter notebook or Google Colab."
        )
        return

    start_time = time()  # Record the start time
    display("Querying R2DT for the RNA image... Please wait.")  # type: ignore
    async with R2dtClient(email) as client:
        job = await client.run(sequence)
        while not (await job.done):
            elapsed_time = time() - start_time  # Calculate elapsed time
            clear_output(wait=True)  # type: ignore
            display(f"Waiting for R2DT... Elapsed time: {elapsed_time:.0f} seconds")  # type: ignore
            await asyncio.sleep(1)

        clear_output(wait=True)  # type: ignore
        display(SVG(await job.result(Format.svg)))  # type: ignore
