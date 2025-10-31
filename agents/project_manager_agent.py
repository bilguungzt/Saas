import json
import os
from pathlib import Path
from agents.router import SmartAIRouter  # <-- THIS IS THE LINE TO FIX
from typing import Union, List

# ---
# THE FIX:
# Python gets confused when you run 'execute_project.py'
# We need to be very explicit about where 'router' is.
# ---
try:
    # This works when running from the main 'execute_project.py'
    from agents.router import SmartAIRouter
except ImportError:
    # This works if you ever try to run this file directly
    from router import SmartAIRouter

class ProjectManagerAgent:
    """
    Orchestrates all agents by first using Gemini to build a
    detailed, routed development plan, and then executing that plan.
    """
    
    def __init__(self, router: SmartAIRouter):
        self.router = router
        self.project_state = {
            "plan": [],
            "generated_files": [],
            "architecture": {},
            "errors": []
        }
        # Get the project's root directory (my_micro_saas/)
        self.base_dir = Path(__file__).resolve().parent.parent
        self.app_dir = self.base_dir / "app"
        
        # Ensure the /app directory exists
        self.app_dir.mkdir(exist_ok=True)
        
        print("✅ ProjectManagerAgent initialized. Ready to build.")
        print(f"Project root set to: {self.base_dir}")

    def _get_development_plan(self, idea: str) -> Union[List[dict], None]:
        """
        Step 1: Ask the "CEO" (Gemini) to create a detailed plan.
        Returns the plan list, or None if it fails.
        """
        print("\n--- [PM] Contacting 'CEO' (Gemini 2.5 Pro) for initial plan... ---")
        
        prompt = f"""
        You are an expert 10x Software Architect. Your job is to create a 
        step-by-step JSON array of tasks to build a new Micro SaaS.

        **The Idea:**
        {idea}

        **Your Task:**
        Break this down into a JSON array of tasks. Each task MUST have 3 keys:
        1. "task_prompt": A detailed, complete prompt for another AI to execute the task.
        2. "output_file": The relative path where the code should be saved (e.g., "app/main.py").
        3. "model": The best model for the job: 'gemini' or 'local'.
        
        **CRITICAL RULE: For *every* task_prompt, you MUST add this exact sentence
        to the end: "CRITICAL: Your response MUST be only the raw, valid, 
        uncommented code for the file. Start with the first line of code 
        and end with the last. Do not include *any* descriptive text, 
        explanations, or markdown formatting."**

        **CRITICAL RULE: When generating 'requirements.txt', you MUST 
        only list the package names. DO NOT pin versions 
        (e.g., use 'fastapi', NOT 'fastapi==0.95.1').**
        **CRITICAL RULE: When generating YAML files (like 'docker-compose.yml'), 
        you MUST ensure the indentation uses 2 spaces and the syntax is perfect.**

        **CRITICAL RULE: When writing Python code inside the 'app/' package,
        you MUST use relative imports to refer to other files in the same
        package (e.g., 'from . import models', NOT 'import models').**
        **CRITICAL RULE: When generating 'requirements.txt', you MUST 
        also include 'python-dotenv' and 'pydantic-settings'.**

        **CRITICAL RULE: When generating the 'app/database.py' file, you MUST
        import and call 'load_dotenv()' from 'dotenv' at the very top of the file
        before any other code runs.**
        **CRITICAL RULE: When generating YAML files (like 'docker-compose.yml'), 
        you MUST ensure the indentation uses 2 spaces and the syntax is perfect.**
        **CRITICAL RULE: When writing Python code inside the 'app/' package,
        you MUST use relative imports (e.g., 'from . import models').**

        **CRITICAL RULE: The 'database.py' file, 'requirements.txt', and 
        '.env' file must all be consistent. If you use 'psycopg2-binary' 
        in requirements, the DATABASE_URL must start with 'postgresql+psycopg2://'.**
        - Use 'gemini' for: High-level architecture, complex logic, or critical files.
        - Use 'local' (Qwen 7B) for: Simple, boilerplate files (like Dockerfiles, requirements.txt,
          or simple utility functions).
        **CRITICAL RULE: When writing Python code inside the 'app/' package,
        you MUST use relative imports (e.g., 'from . import models').**

        **CRITICAL RULE: You MUST ensure all database credentials (username, 
        password, dbname) are consistent across the '.env.example', 
        'docker-compose.yml', and 'database.py' files. 
        Use 'myuser', 'mypassword', and 'mydatabase'.**

        **CRITICAL RULE: All Pydantic models in 'schemas.py' MUST 
        use Pydantic V2 config (model_config = {{"from_attributes": True}}) 
        instead of the old V1 'Config' class with 'orm_mode'.**
        **Example JSON Format:**
        **CRITICAL RULE: When writing Python code inside the 'app/' package,
        you MUST use relative imports (e.g., 'from . import models').**

        **CRITICAL RULE: The 'database.py' file, 'requirements.txt', and 
        '.env' file must all be consistent. If you use 'psycopg2-binary' 
        in requirements, the DATABASE_URL must start with 'postgresql+psycopg2://'.**

        **CRITICAL RULE: The 'requirements.txt' file MUST include
        'python-dotenv' and 'pydantic-settings' for all projects.**

        **CRITICAL RULE: If the project involves users or passwords, 
        the 'requirements.txt' file MUST also include 'passlib[bcrypt]'.**
        [
          {{"task_prompt": "Generate a 'requirements.txt' file for a FastAPI app, including 'fastapi', 'uvicorn', 'sqlalchemy', and 'psycopg2-binary'. IMPORTANT: Your response MUST be only the raw, valid content for this file. Do not add *any* other text, explanations, comments, or markdown fences like ```.", "output_file": "app/requirements.txt", "model": "local"}}
        ]
        
        Output *only* the JSON array and nothing else.
        """
        
        plan_json_str = self.router.query(prompt, model_type="gemini")
        
        if plan_json_str is None:
            print("---! CRITICAL ERROR: Could not generate development plan from Gemini. !---")
            return None

        try:
            clean_json_str = plan_json_str.strip().lstrip('```json').rstrip('```')
            plan = json.loads(clean_json_str)
            print(f"✅ ...[PM]: Development plan with {len(plan)} steps received from Gemini.")
            self.project_state['plan'] = plan
            return plan
        except json.JSONDecodeError:
            print("---! CRITICAL ERROR: Gemini did not return valid JSON for the plan. !---")
            print(f"Received: {plan_json_str}")
            return None

    def build_complete_app(self, idea: str):
        """
        Orchestrates the entire app development based on the plan.
        """
        print("🚀 Starting AI-driven development...\n")
        
        development_plan = self._get_development_plan(idea)
        
        if not development_plan: 
            print("Build failed: No development plan created.")
            return

        print(f"\n⚙️  Starting Execution of {len(development_plan)} tasks...")
        
        for i, task in enumerate(development_plan):
            print(f"\n--- Task {i+1}/{len(development_plan)} ---")
            print(f"  Task: {task['task_prompt'][:50]}...")
            print(f"  File: {task['output_file']}")
            print(f"  Agent: {task['model']}")
            
            generated_content = self.router.query(
                prompt=task['task_prompt'],
                model_type=task['model']
            )
            
            if generated_content is None:
                print(f"  ---! CRITICAL: Task {i+1} failed. Build halted. !---")
                self.project_state['errors'].append(task)
                break 
            
            try:
                output_path = self.base_dir / task['output_file']
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_path, 'w') as f:
                    f.write(generated_content)
                    
                print(f"  ✓ File saved: {task['output_file']}")
                self.project_state['generated_files'].append(task['output_file'])

            except Exception as e:
                print(f"  ---! Task Failed (File Save Error): {e} !---")
                self.project_state['errors'].append(task)
                break 
        
        if self.project_state['errors']:
            print(f"\n🔥🔥🔥 AI Build FAILED with {len(self.project_state['errors'])} error(s). 🔥🔥🔥")
        else:
            print("\n🎉🎉🎉 AI Build Complete! 🎉🎉🎉")
            print("Check your '/app' folder for the generated code.")
        
        report_path = self.base_dir / "project_build_report.json"
        with open(report_path, 'w') as f:
            json.dump(self.project_state, f, indent=2)
            
        print(f"Build report saved to: {report_path.name}")