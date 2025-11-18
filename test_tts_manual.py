"""Manual test script for Doubao TTS blocks."""
import asyncio
import sys
sys.path.insert(0, '/app/workspace/tasks/submit-doubao-tts')
sys.path.insert(0, '/app/workspace/tasks/get-doubao-tts-result')

from tasks.submit_doubao_tts import __init__ as submit_tts
from tasks.get_doubao_tts_result import __init__ as get_tts_result
from oocana import Context

class MockContext:
    """Mock context for testing."""
    async def oomol_token(self):
        # This would need a real token from the OOMOL system
        return "mock_token"

    def report_progress(self, progress):
        print(f"Progress: {progress}%")

async def test_tts_flow():
    """Test the complete TTS flow."""
    context = MockContext()

    # Step 1: Submit TTS request
    print("Step 1: Submitting TTS request...")
    submit_params = {
        "text": "让我把这段文字读给你听",
        "voice": "zh_female_xueayi_saturn_bigtts"
    }

    try:
        submit_result = await submit_tts.main(submit_params, context)
        print(f"Submit result: {submit_result}")

        if "task_id" in submit_result:
            task_id = submit_result["task_id"]
            print(f"Task ID: {task_id}")

            # Step 2: Get TTS result
            print("\nStep 2: Polling for TTS result...")
            get_params = {
                "task_id": task_id,
                "max_retries": 30,
                "poll_interval": 2
            }

            get_result = await get_tts_result.main(get_params, context)
            print(f"Get result: {get_result}")

            if "audio_url" in get_result and get_result["audio_url"]:
                print(f"\nSuccess! Audio URL: {get_result['audio_url']}")
            else:
                print(f"\nFailed to get audio URL. Full result: {get_result}")
        else:
            print("Failed to get task_id from submit response")

    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_tts_flow())
