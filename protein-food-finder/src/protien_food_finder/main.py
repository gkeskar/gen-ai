#!/usr/bin/env python
import sys
import os
import warnings

from datetime import datetime
from dotenv import load_dotenv

from protien_food_finder.crew import ProtienFoodFinder

# Load environment variables from .env file
load_dotenv()

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Validate required API keys are set
def validate_api_keys():
    """Validate that required API keys are configured."""
    missing_keys = []
    
    if not os.getenv("GOOGLE_API_KEY"):
        missing_keys.append("GOOGLE_API_KEY")
    if not os.getenv("SERPER_API_KEY"):
        missing_keys.append("SERPER_API_KEY")
    
    if missing_keys:
        raise ValueError(
            f"Missing required API keys: {', '.join(missing_keys)}\n"
            f"Please set them in your .env file or environment variables."
        )
    
    print("✅ API keys validated successfully\n")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the protein food finder crew.
    """
    # Validate API keys before running
    validate_api_keys()
    
    inputs = {
        'location': 'Belmont, CA 94002',
        'dietary_preferences': '''
        - High protein 
        - No Beef or pork, 
        - chichen and fish, eggs are allowed
        - Gluten-free
        - No sugar added
        - frozen and shelf stable products are allowed
        '''
    }
    
    try:
        print("\n" + "="*80)
        print("🚀 Starting Protein Food Finder Crew")
        print("="*80 + "\n")
        print(f"📍 Location: {inputs['location']}")
        print(f"🥗 Dietary Preferences: {inputs['dietary_preferences']}")
        print("\n" + "="*80 + "\n")
        
        result = ProtienFoodFinder().crew().kickoff(inputs=inputs)
        
        print("\n" + "="*80)
        print("✅ CREW EXECUTION COMPLETED")
        print("="*80 + "\n")
        
        print("📊 FINAL RESULTS:")
        print("-" * 80)
        print(result)
        print("-" * 80 + "\n")
        
        # If result has tasks_output, print each task result
        if hasattr(result, 'tasks_output') and result.tasks_output:
            print("\n" + "="*80)
            print("📋 INDIVIDUAL TASK OUTPUTS")
            print("="*80 + "\n")
            
            for i, task_output in enumerate(result.tasks_output, 1):
                print(f"\n{'='*80}")
                print(f"Task {i}: {task_output.description if hasattr(task_output, 'description') else 'N/A'}")
                print(f"{'='*80}")
                print(f"Agent: {task_output.agent if hasattr(task_output, 'agent') else 'N/A'}")
                print(f"\nOutput:")
                print("-" * 80)
                print(task_output.raw if hasattr(task_output, 'raw') else task_output)
                print("-" * 80 + "\n")
        
        return result
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    # Validate API keys before training
    validate_api_keys()
    
    inputs = {
        'location': 'Belmont, CA 94002',
        'dietary_preferences': '''
        - High protein goal: 20g+ per serving
        - No dietary restrictions
        '''
    }
    try:
        ProtienFoodFinder().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    # Validate API keys before replaying
    validate_api_keys()
    
    try:
        ProtienFoodFinder().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    # Validate API keys before testing
    validate_api_keys()
    
    inputs = {
        'location': 'Belmont, CA 94002',
        'dietary_preferences': '''
        - High protein goal: 20g+ per serving
        - No dietary restrictions
        '''
    }
    
    try:
        ProtienFoodFinder().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
