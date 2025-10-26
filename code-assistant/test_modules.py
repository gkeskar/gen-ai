"""
Simple test script to verify the modules work correctly before adding UI
"""
import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from project root
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

# Set OpenAI configuration - get from environment
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

os.environ['OPENAI_API_KEY'] = openai_api_key
os.environ['OPENAI_BASE_URL'] = "https://ai-gateway.zende.sk/v1"

print(f"✓ Loaded OpenAI API Key: {openai_api_key[:10]}...")
print(f"✓ Using Gateway: https://ai-gateway.zende.sk/v1\n")

from learning_manager import LearningManager


async def test_basic_analysis():
    """Test analyzing a simple Python file"""
    manager = LearningManager()
    
    # Test with this very file
    file_path = "test_modules.py"
    
    print("🧪 Testing Code Learning Assistant Modules")
    print("=" * 50)
    print(f"Analyzing file: {file_path}\n")
    
    final_result = None
    async for status in manager.analyze_code(
        file_path=file_path,
        task_description="Testing the code learning assistant system",
        include_git_diff=False
    ):
        print(f"📝 {status}")
        # The last item will be the final result
        final_result = status
    
    return final_result


if __name__ == "__main__":
    print("Starting module test...\n")
    result = asyncio.run(test_basic_analysis())
    print("\n✅ Module test complete!")

