import os
from pathlib import Path
from dotenv import load_dotenv

# ---
# This loads your .env file *before* the router is imported.
# This is critical to ensure the API key is ready.
# ---
load_dotenv() 

from router import SmartAIRouter # <-- This import must come AFTER load_dotenv()

# ---
# V2 CONTROL PANEL
# ---
# 1. Choose your model:
#    'gemini' -> Your "CEO". This is a complex new feature.
MODEL_TO_USE = "gemini" 

# 2. Define your task:
YOUR_PROMPT = """
I need to add a new 'GET /posts' endpoint to 'app/main.py'.

This endpoint should:
1. Take 'skip' and 'limit' query parameters, with defaults of 0 and 10.
2. Import a new function 'get_posts' from 'app/crud.py'.
3. Call 'get_posts(db=db, skip=skip, limit=limit)'.
4. Return a list of 'schemas.Post' objects.
5. Also, I need the 'get_posts' function added to 'app/crud.py'. This function 
   should query and return all posts from the 'models.Post' table, using 
   skip and limit for pagination.

IMPORTANT: You must modify *two* files. Your response must contain
the complete, new 'app/crud.py' file first, followed by the
complete, new 'app/main.py' file that includes the new endpoint.

CRITICAL: Your response MUST be only the raw, valid code. 
Do not add *any* other text, explanations, or markdown fences like ```.
"""

# 3. Define the output file:
#    Since the AI is generating two files, we'll save its raw
#    response to a text file for you to copy/paste from.
OUTPUT_FILENAME = "agent_output_new_features.txt"
# ---
# End of Control Panel
# ---


def main():
    """
    This is the main "engine" of your control panel.
    """
    # Make sure your Ollama app is running!
    router = SmartAIRouter()
    
    print(f"Starting task: {YOUR_PROMPT[:50]}...")
    
    generated_content = router.query(YOUR_PROMPT, model_type=MODEL_TO_USE)
    
    if generated_content:
        print("\n--- 🚀 AI-Generated Content: 🚀 ---")
        print(generated_content)
        
        # Save the output to the root project folder
        base_dir = Path(__file__).resolve().parent.parent
        output_path = base_dir / OUTPUT_FILENAME
        
        with open(output_path, 'w') as f:
            f.write(generated_content)
            
        print(f"\n--- ✅ Content successfully saved to {output_path.name} ---")
        print("\nACTION REQUIRED: Open 'agent_output_new_features.txt' and copy the code into 'app/crud.py' and 'app/main.py'.")

# ---
# This is the "engine starter" that was missing.
# It tells Python to run the `main` function when you execute the script.
# ---
if __name__ == "__main__":
    main()