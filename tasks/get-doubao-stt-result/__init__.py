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
    max_retries = params.get("max_retries", 30)
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

            # Print the response for debugging
            print(f"[DEBUG] Retry {retry_count + 1}/{max_retries}, Response: {result}")

            # Get state from response
            state = result.get("state", "unknown")

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

            context.report_progress(100)

            return {
                "text": text,
                "words": utterances,
                "full_result": result
            }

        except requests.exceptions.RequestException as e:
            # Network error, retry
            print(f"[DEBUG] Request error: {e}, retrying...")
            retry_count += 1
            if retry_count < max_retries:
                time.sleep(poll_interval)
            continue

    # Max retries reached
    return {
        "text": "",
        "words": [],
        "full_result": {"error": f"Max retries ({max_retries}) reached"}
    }
