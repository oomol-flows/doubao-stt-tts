from oocana import Context

#region generated meta
import typing
class Inputs(typing.TypedDict):
    saved_path: str | None
class Outputs(typing.TypedDict):
    saved_path: typing.NotRequired[str | None]
#endregion

async def main(params: Inputs, context: Context) -> Outputs | None:

    # 如果 saved_path 为 None，使用默认路径
    if params["saved_path"] is None:
        saved_path = f"{context.session_dir}/new_audio.mp3"
    else:
        saved_path = params["saved_path"]
    
    # 返回处理后的路径
    return {"saved_path": saved_path}