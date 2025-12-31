#region generated meta
import typing
class Inputs(typing.TypedDict):
    task_id: str
    max_retries: float | None
    poll_interval: float | None
class Outputs(typing.TypedDict):
    audio_url: typing.NotRequired[str]
    full_result: typing.NotRequired[dict]
#endregion

from oocana import Context
import requests
import time
import datetime

async def main(params: Inputs, context: Context) -> Outputs:
    """Poll and retrieve the TTS result from Doubao service."""

    task_id = params["task_id"]
    max_retries = params.get("max_retries", 30)
    poll_interval = params.get("poll_interval", 2)

    url = f"https://fusion-api.oomol.com/v1/doubao-tts/result/{task_id}"

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
            t = datetime.datetime.now()
            print(f"[DEBUG {t}] Retry {retry_count + 1}/{max_retries}, Response: {result}")

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

            # State is not 'processing', extract data from result
            # The audio URL might be in different fields depending on API response structure
            data = result.get("data", {})

            # Try different possible fields for audio URL
            audio_url = None
            if "audioURL" in data:
                audio_url = data["audioURL"]
            elif "audio_url" in data:
                audio_url = data["audio_url"]
            elif "url" in data:
                audio_url = data["url"]
            elif "audioURL" in result:
                audio_url = result["audioURL"]
            elif "audio_url" in result:
                audio_url = result["audio_url"]
            elif "url" in result:
                audio_url = result["url"]
            else:
                # If no audio URL found, return the full result
                audio_url = ""

            context.report_progress(100)

            return {
                "audio_url": audio_url,
                "full_result": result
            }

        except requests.exceptions.Timeout as e:
            # Timeout error
            print(f"[DEBUG] Request timeout: {e}, retrying...")
            retry_count += 1
            if retry_count < max_retries:
                time.sleep(poll_interval)
                continue
            error_msg = f"Request timeout after {max_retries} retries"
            print(f"[ERROR] {error_msg}")
            raise TimeoutError(error_msg) from e

        except requests.exceptions.HTTPError as e:
            # HTTP error (4xx, 5xx)
            error_msg = f"HTTP Error {response.status_code}: {response.text}"
            print(f"[ERROR] {error_msg}")
            raise ValueError(error_msg) from e

        except requests.exceptions.RequestException as e:
            # Other network errors, retry
            print(f"[DEBUG] Request error: {e}, retrying...")
            retry_count += 1
            if retry_count < max_retries:
                time.sleep(poll_interval)
                continue
            error_msg = f"Network error after {max_retries} retries: {str(e)}"
            print(f"[ERROR] {error_msg}")
            raise ConnectionError(error_msg) from e

    # Max retries reached (processing state timeout)
    error_msg = f"TTS task still processing after {max_retries} retries (timeout)"
    print(f"[ERROR] {error_msg}")
    raise TimeoutError(error_msg)
