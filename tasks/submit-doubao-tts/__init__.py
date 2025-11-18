#region generated meta
import typing
class Inputs(typing.TypedDict):
    text: str
    voice: typing.Literal["zh_male_lengkugege_emo_v2_mars_bigtts", "zh_female_tianxinxiaomei_emo_v2_mars_bigtts", "zh_female_gaolengyujie_emo_v2_mars_bigtts", "zh_male_aojiaobazong_emo_v2_mars_bigtts", "zh_male_guangzhoudege_emo_mars_bigtts", "zh_male_jingqiangkanye_emo_mars_bigtts", "zh_female_linjuayi_emo_v2_mars_bigtts", "zh_male_yourougongzi_emo_v2_mars_bigtts", "zh_male_ruyayichen_emo_v2_mars_bigtts", "zh_male_junlangnanyo_emo_v2_mars_bigtts", "zh_male_beijingxiaoye_emo_v2_mars_bigtts", "zh_female_roumeinvyou_emo_v2_mars_bigtts", "zh_male_yangguangqingnian_emo_v2_mars_bigtts", "zh_female_meilinvyou_emo_v2_mars_bigtts", "zh_male_shenyeboke_emo_v2_mars_bigtts", "en_female_candice_emo_v2_mars_bigtts", "en_female_skye_emo_v2_mars_bigtts", "en_male_glen_emo_v2_mars_bigtts", "en_male_sylus_emo_v2_mars_bigtts", "en_male_corey_emo_v2_mars_bigtts", "en_female_nadia_tips_emo_v2_mars_bigtts"]
class Outputs(typing.TypedDict):
    task_id: typing.NotRequired[str]
#endregion

from oocana import Context
import requests

async def main(params: Inputs, context: Context) -> Outputs:
    """Submit text to Doubao TTS service."""

    url = "https://fusion-api.oomol.com/v1/doubao-tts/submit"

    # Get OOMOL token for authorization
    token = await context.oomol_token()

    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }

    payload = {
        "text": params["text"],
        "voice": params["voice"]
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30.0)

        # Print response for debugging
        print(f"[DEBUG] Response status: {response.status_code}")
        print(f"[DEBUG] Response body: {response.text}")

        response.raise_for_status()

        result = response.json()

        # Extract task ID from response
        # API may return different formats, handle multiple cases
        if "taskId" in result:
            task_id = result["taskId"]
        elif "data" in result and "taskId" in result["data"]:
            task_id = result["data"]["taskId"]
        elif "id" in result:
            task_id = result["id"]
        elif "data" in result and "id" in result["data"]:
            task_id = result["data"]["id"]
        else:
            raise ValueError(f"Unexpected response format: {result}")

        return {"task_id": task_id}

    except requests.exceptions.HTTPError as e:
        error_msg = f"HTTP Error {response.status_code}: {response.text}"
        print(f"[ERROR] {error_msg}")
        raise ValueError(error_msg) from e
