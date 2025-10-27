
from agents import Agent, Runner, function_tool, transfer_to_agent
from tools import read_code_file, save_learning_doc, get_git_diff
import specialist_agents
from typing import Optional
import asyncio


# Convert specialist agents to tools
@function_tool
async def language_teacher_tool(input: str) -> str:
    """Explain programming language concepts used in the code"""
    result = await Runner.run(specialist_agents.language_teacher, input)
    return str(result.final_output)


@function_tool
async def code_explainer_tool(input: str) -> str:
    """Explain what the code does and how it works"""
    result = await Runner.run(specialist_agents.code_explainer, input)
    return str(result.final_output)


@function_tool
async def change_documenter_tool(input: str) -> str:
    """Document the changes and implementation approach"""
    result = await Runner.run(specialist_agents.change_documenter, input)
    return str(result.final_output)


@function_tool
async def git_diff_analyzer_tool(input: str) -> str:
    """Analyze git diff output to explain what specifically changed"""
    result = await Runner.run(specialist_agents.git_diff_analyzer, input)
    return str(result.final_output)


# Documentation Manager - Main orchestrator
documentation_manager_instructions = """You help developers learn and document their code work.

When given a file to analyze:

1. **Read the code**: Use read_code_file to get the actual file content

2. **Call Language Teacher**: 
   CRITICAL: Pass the COMPLETE file content in this format:
   
   "Teach me about the programming language concepts in this code. Here's the full code:
   
   ```[language]
   [PASTE THE ENTIRE CODE FILE HERE - ALL LINES]
   ```
   
   REQUIREMENTS:
   - Quote actual code snippets from above with line numbers
   - Use analogies (e.g., 'think of this like...')
   - Compare to Python/JavaScript syntax
   - Explain WHY these features exist
   - Share common mistakes beginners make
   - Give practical pro tips
   
   Be SPECIFIC to THIS code, not generic!"

3. **Call Code Explainer**: 
   Pass the COMPLETE file content:
   
   "Explain how this code works step-by-step. Here's the full code:
   
   ```[language]
   [PASTE THE ENTIRE CODE FILE HERE - ALL LINES]
   ```
   
   REQUIREMENTS:
   - Start with big picture (what does this code do?)
   - Walk through each major function/method
   - Show data flow with arrows (input → process → output)
   - Quote actual code snippets
   - Explain the 'why' behind design choices"

4. **Call Change Documenter**: 
   Pass the COMPLETE file content with task context asking for PR-ready documentation

5. **Optionally analyze git history** (if requested):
   - Use get_git_diff with include_commit_history=True to get both diff and commit history
   - Pass the combined output to git_diff_analyzer_tool for comprehensive analysis of:
     * How the file evolved over time (from commit history)
     * What specific changes were made (from diff)
     * Why changes were made (inferred from commit messages)

6. **Combine everything** into a comprehensive learning document using this structure:

   # [File Name] - Learning Documentation
   
   ## 📚 Language Concepts Explained
   [Full output from Language Teacher - should include code snippets, analogies, comparisons]
   
   ## 🔍 How The Code Works
   [Full output from Code Explainer - should include step-by-step walkthrough with data flow]
   
   ## 📝 Implementation Documentation
   [Full output from Change Documenter - PR-ready documentation]
   
   ## 📜 Code Evolution & History (if git analysis requested)
   [Commit history showing how the file evolved]
   [Git diff analysis with detailed line-by-line changes]
   [Insights about why changes were made based on commit messages]

7. **Use save_learning_doc** to save the final document

CRITICAL RULES:
- ALWAYS pass the FULL code file content to each specialist agent
- NEVER summarize or truncate the code  
- Each agent needs the COMPLETE code to analyze properly
- The specialist outputs should be DETAILED (multiple paragraphs per concept)
- If outputs seem generic or short, the agents didn't get the full code!"""

# Gather all tools
tools = [
    read_code_file,
    get_git_diff,
    language_teacher_tool,
    code_explainer_tool,
    change_documenter_tool,
    git_diff_analyzer_tool,
    save_learning_doc
]

documentation_manager = Agent(
    name="Documentation Manager",
    instructions=documentation_manager_instructions,
    tools=tools,
    model="gpt-4o"  # Using powerful model to ensure it follows complex instructions
)


class LearningManager:
    """Main manager for code learning and documentation"""
    
    async def analyze_code(
        self, 
        file_path: str, 
        task_description: str = "",
        include_git_diff: bool = False,
        include_commit_history: bool = False
    ):
        """
        Analyze and document a code file for learning and PR documentation
        
        Args:
            file_path: Path to the code file to analyze
            task_description: Context about what was done (e.g., "Added ADPP changes")
            include_git_diff: Whether to include git diff analysis
            include_commit_history: Whether to include commit history analysis
        """
        
        yield "Starting code analysis..."
        
        # Build the analysis workflow based on whether git analysis is included
        if include_git_diff or include_commit_history:
            # Git-diff-first workflow (better for code review)
            workflow = self._build_git_first_workflow(file_path, task_description, include_commit_history)
            yield "Using git-first analysis workflow (recommended for code review)"
        else:
            # Standard workflow (learning new code)
            workflow = self._build_standard_workflow(file_path, task_description)
            yield "Using standard learning workflow"
        
        yield "Analyzing file and generating documentation..."
        
        result = await Runner.run(documentation_manager, workflow)
        
        # Don't yield "Documentation complete!" here - the UI will add it when displaying final result
        yield result.final_output
    
    def _build_git_first_workflow(self, file_path: str, task_description: str, include_commit_history: bool) -> str:
        """Build a git-diff-first workflow for code review"""
        return f"""Please analyze this code change for review: {file_path}

Task context: {task_description}

🔍 **CODE REVIEW WORKFLOW** (Git-First Approach):

STEP 1: Use read_code_file to get the current code state

STEP 2: Use get_git_diff with file_path='{file_path}' and include_commit_history={include_commit_history}
   This shows WHAT changed and WHY (from commit messages)

STEP 3: Pass git output to git_diff_analyzer_tool for detailed change analysis
   Focus on: What changed? Why? Impact? Risks?

STEP 4: Based on the changes identified, use code_explainer_tool to explain:
   - How the changed sections work
   - Data flow through modified code
   - Integration with surrounding code

STEP 5: Use language_teacher_tool ONLY for new language features/patterns introduced in the changes
   - Focus on language concepts specific to what changed
   - Compare to other languages if relevant

STEP 6: Use change_documenter_tool to create PR-ready documentation

FINAL STEP: Use save_learning_doc to save the review documentation

**CRITICAL**: This is a CODE REVIEW, not generic learning. Focus on:
- WHAT specific lines changed (from diff)
- WHY they changed (from commit messages)
- HOW the changes work (from code analysis)
- RISKS and testing needs (from change analysis)

Structure the output for an engineer reviewing this code change."""

    def _build_standard_workflow(self, file_path: str, task_description: str) -> str:
        """Build standard workflow for learning new code"""
        return f"""Please analyze and document this code file: {file_path}

Task context: {task_description}

📚 **LEARNING WORKFLOW** (Understanding New Code):

STEP 1: Use read_code_file tool to read the actual file content

STEP 2: Use language_teacher_tool to explain the programming concepts
   - Language features used
   - Patterns and idioms
   - Comparisons to other languages

STEP 3: Use code_explainer_tool to explain what the code actually does
   - Step-by-step walkthrough
   - Data flow
   - Design decisions

STEP 4: Use change_documenter_tool to document the implementation approach

FINAL STEP: Use save_learning_doc tool to save the documentation

**Focus**: Help someone LEARN this codebase from scratch.
- Explain language concepts
- Walk through how it works
- Provide context and best practices

Structure the output for learning and understanding."""
    
    
    async def analyze_multiple_files(
        self,
        file_paths: list,
        project_description: str = ""
    ):
        """Analyze multiple files in batch"""
        for i, file_path in enumerate(file_paths, 1):
            yield f"Processing file {i}/{len(file_paths)}: {file_path}"
            
            async for status in self.analyze_code(file_path, project_description):
                yield status
        
        yield f"Completed analysis of {len(file_paths)} files"

