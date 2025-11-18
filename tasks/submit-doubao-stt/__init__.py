#region generated meta
import typing
class Inputs(typing.TypedDict):
    audio_url: str
    format: str
class Outputs(typing.TypedDict):
    task_id: typing.NotRequired[str]
#endregion

from oocana import Context
import requests

async def main(params: Inputs, context: Context) -> Outputs:
    """Submit audio file to Doubao STT service."""

    url = "https://fusion-api.oomol.com/v1/doubao-stt/submit"

    # Get OOMOL token for authorization
    token = await context.oomol_token()

    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }

    payload = {
        "audioURL": params["audio_url"],
        "format": params["format"]
    }

    response = requests.post(url, json=payload, headers=headers, timeout=30.0)
    response.raise_for_status()

    result = response.json()

    # Extract task ID from response
    # API returns sessionID in the response
    if "sessionID" in result:
        task_id = result["sessionID"]
    elif "data" in result and "sessionID" in result["data"]:
        task_id = result["data"]["sessionID"]
    elif "data" in result and "taskId" in result["data"]:
        task_id = result["data"]["taskId"]
    elif "taskId" in result:
        task_id = result["taskId"]
    else:
        raise ValueError(f"Unexpected response format: {result}")

    return {"task_id": task_id}
