# --- FIX 1: Add these two lines at the VERY TOP ---
from dotenv import load_dotenv
load_dotenv()

# --- FIX 2: Change this import (remove 'agents.') ---
from router import SmartAIRouter
import os
from pathlib import Path

# ---
# V1 CONTROL PANEL
# ---
# 1. Choose your model:
#    'gemini' -> Your "CEO". Use for complex tasks (architecture, hard logic).
#    'local'  -> Your "Intern". Use for simple tasks (Dockerfile, simple functions).
MODEL_TO_USE = "local" 

# 2. Define your task:
YOUR_PROMPT = """
Generate a 'Dockerfile' for our FastAPI application in 'app/main.py'.
The 'requirements.txt' is in the same directory ('app/').

Requirements:
- Use an official Python 3.11-slim base image.
- Use a multi-stage build to keep the final image small.
- Create a non-root user to run the app.
- Copy in the 'app/' directory.
- Expose port 8000.
- The command to run the app is: uvicorn main:app --host 0.0.0.0 --port 8000
"""

# 3. Define the output file (relative to the 'my_micro_saas' folder):
OUTPUT_FILENAME = "Dockerfile"
# ---
# End of Control Panel
# ---


def main():
    # Make sure your Ollama app is running!
    router = SmartAIRouter()
    
    print(f"Starting task: {YOUR_PROMPT[:50]}...")
    
    generated_content = router.query(YOUR_PROMPT, model_type=MODEL_TO_USE)
    
    if generated_content:
        print("\n--- 🚀 AI-Generated Content: 🚀 ---")
        print(generated_content)
        
        # Save the output to the root project folder (my_micro_saas/Dockerfile)
        base_dir = Path(__file__).resolve().parent.parent
        output_path = base_dir / OUTPUT_FILENAME
        
        with open(output_path, 'w') as f:
            f.write(generated_content)
            
        print(f"\n--- ✅ Content successfully saved to {output_path.name} ---")

if __name__ == "__main__":
    main()