#region generated meta
import typing
class Inputs(typing.TypedDict):
    task_id: str
    max_retries: float | None
    poll_interval: float | None
class Outputs(typing.TypedDict):
    text: typing.NotRequired[str]
    words: typing.NotRequired[list[typing.Any]]
    full_result: typing.NotRequired[dict]
#endregion

from oocana import Context
import requests
import time

async def main(params: Inputs, context: Context) -> Outputs:
    """Poll and retrieve the STT result from Doubao service."""

    task_id = params["task_id"]
    max_retries = params.get("max_retries", 900)
    poll_interval = params.get("poll_interval", 2)

    url = f"https://fusion-api.oomol.com/v1/doubao-stt/result/{task_id}"

    # Get OOMOL token for authorization
    token = await context.oomol_token()

    headers = {
        "Authorization": token
    }

    retry_count = 0

    while retry_count < max_retries:
        try:
            response = requests.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()

            result = response.json()

            # Get state from response
            state = result.get("state", "unknown")

            # Print status for debugging
            print(f"[STT Polling] Attempt {retry_count + 1}/{max_retries} - State: {state}")

            # If state is 'processing', continue polling
            if state == "processing":
                progress = min(int((retry_count / max_retries) * 90), 90)
                context.report_progress(progress)

                retry_count += 1
                if retry_count < max_retries:
                    time.sleep(poll_interval)
                continue

            # State is not 'processing', extract data from result.data
            data = result.get("data", {})
            text = data.get("text", "")
            utterances = data.get("utterances", [])

            print(f"[STT Polling] Task completed - State: {state}, Text length: {len(text)} chars, Utterances: {len(utterances)}")

            context.report_progress(100)

            return {
                "text": text,
                "words": utterances,
                "full_result": result
            }

        except requests.exceptions.RequestException as e:
            retry_count += 1
            if retry_count < max_retries:
                time.sleep(poll_interval)
                continue

    raise TimeoutError(f"STT task still processing after {max_retries} retries (timeout)")
