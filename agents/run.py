import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv() 
from router import SmartAIRouter # <-- This import must come AFTER load_dotenv()

# ---
# V2.1 CONTROL PANEL
# ---
# 1. Choose your model:
#    'gemini' -> Your "CEO". This is a complex new feature.
MODEL_TO_USE = "gemini" 

# 2. Define your task:
YOUR_PROMPT = """
I need to add one new function to 'app/crud.py'.

The function should be:
def get_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Post).offset(skip).limit(limit).all()

IMPORTANT: Your response MUST be only the raw, valid Python code for this
*single function*. Do not add *any* other text, explanations,
comments, or markdown fences like ```.
"""

# 3. Define the output file:
OUTPUT_FILENAME = "agent_output_get_posts_func.txt"
# ---
# End of Control Panel
# ---


def main():
    """
    This is the main "engine" of your control panel.
    """
    router = SmartAIRouter()
    print(f"Starting task: {YOUR_PROMPT[:50]}...")
    generated_content = router.query(YOUR_PROMPT, model_type=MODEL_TO_USE)
    
    if generated_content:
        print("\n--- 🚀 AI-Generated Content: 🚀 ---")
        print(generated_content)
        
        base_dir = Path(__file__).resolve().parent.parent
        output_path = base_dir / OUTPUT_FILENAME
        
        with open(output_path, 'w') as f:
            f.write(generated_content)
            
        print(f"\n--- ✅ Content successfully saved to {output_path.name} ---")
        print(f"\nACTION REQUIRED: Open '{OUTPUT_FILENAME}' and copy the new")
        print(f"function into the bottom of your 'app/crud.py' file.")

if __name__ == "__main__":
    main()