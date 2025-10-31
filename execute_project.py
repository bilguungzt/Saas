import os
from dotenv import load_dotenv
from agents.router import SmartAIRouter
from agents.project_manager_agent import ProjectManagerAgent

# Load .env file (GEMINI_API_KEY) from the root
load_dotenv()

# ---
# THIS IS YOUR "CEO'S" MAIN PROMPT
# Define the entire project you want to build.
# ---
YOUR_BIG_IDEA = """
Build a simple FastAPI backend for a blog.
It needs to:
1. Have a PostgreSQL database.
2. Have two tables: 'users' (with email, hashed_password) and 'posts' (with title, content, owner_id).
3. Have a 'main.py' that connects to the database.
4. Have a '/users' endpoint to create a new user.
5. Have a '/posts' endpoint to create a new post.
"""
# ---
# End of prompt
# ---

def main():
    # 1. Initialize the "phone system"
    #    (Make sure your Ollama app is running!)
    router = SmartAIRouter()
    
    # 2. Initialize the "AI Project Manager"
    pm = ProjectManagerAgent(router)
    
    # 3. Give the PM the "Big Idea" and tell it to start
    pm.build_complete_app(idea=YOUR_BIG_IDEA)

if __name__ == "__main__":
    main()