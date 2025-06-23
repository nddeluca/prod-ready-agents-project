#!/usr/bin/env python3
"""
VimGolf Problem Solver using OpenAI

This script presents 10 curated VimGolf challenges to an LLM and asks it to solve them
by generating the minimal Vim command sequences needed to transform the input text.
"""

import os
import sys
from typing import Dict, List, Tuple
from dataclasses import dataclass
from openai import OpenAI


@dataclass
class VimGolfProblem:
    """Represents a VimGolf challenge"""
    id: str
    title: str
    description: str
    start_text: str
    end_text: str
    best_score: int = None


class VimGolfSolver:
    """Solves VimGolf problems using OpenAI"""
    
    def __init__(self, api_key: str = None):
        """Initialize with OpenAI API key"""
        self.client = OpenAI(api_key=api_key or os.getenv('OPENAI_API_KEY'))
        self.problems = self._load_problems()
    
    def _load_problems(self) -> List[VimGolfProblem]:
        """Load the 10 curated VimGolf problems"""
        return [
            VimGolfProblem(
                id="9v00669b3ff1",
                title="Rearrange array to single level",
                description="Flatten nested array structure and remove empty elements",
                start_text="[[1,2],[3,4,[]],[5,6,[7,8]]]",
                end_text="[1,2,3,4,5,6,7,8]"
            ),
            VimGolfProblem(
                id="9v00680e54330", 
                title="Create json from a .env file",
                description="Convert environment variables to JSON format",
                start_text="API_KEY=abc123\nDATABASE_URL=postgres://localhost\nDEBUG=true",
                end_text='{\n  "API_KEY": "abc123",\n  "DATABASE_URL": "postgres://localhost",\n  "DEBUG": "true"\n}'
            ),
            VimGolfProblem(
                id="9v0067a47b9200",
                title="Reordering properties", 
                description="Sort CSS properties by line length",
                start_text="color: red;\nbackground-color: blue;\nmargin: 10px;\npadding-top: 5px;",
                end_text="margin: 10px;\ncolor: red;\npadding-top: 5px;\nbackground-color: blue;"
            ),
            VimGolfProblem(
                id="9v00674f1bfb00",
                title="YAML to dotenv",
                description="Convert YAML configuration to .env format", 
                start_text="database:\n  host: localhost\n  port: 5432\napi:\n  key: secret",
                end_text="DATABASE_HOST=localhost\nDATABASE_PORT=5432\nAPI_KEY=secret"
            ),
            VimGolfProblem(
                id="9v0067255515",
                title="Nested JSON Flattener",
                description="Transform deeply nested JSON to dot-notation",
                start_text='{"user": {"name": "John", "settings": {"theme": "dark"}}}',
                end_text='{"user.name": "John", "user.settings.theme": "dark"}'
            ),
            VimGolfProblem(
                id="9v0066d89856",
                title="Fix timezone format",
                description="Add 'T' and 'Z' to datetime strings",
                start_text="2023-10-15 14:30:00\n2023-10-16 09:15:30",
                end_text="2023-10-15T14:30:00Z\n2023-10-16T09:15:30Z"
            ),
            VimGolfProblem(
                id="9v0067056336", 
                title="Change class fields from camel case to snake case",
                description="Convert camelCase variable names to snake_case",
                start_text="firstName = 'John'\nlastName = 'Doe'\nphoneNumber = '555-1234'",
                end_text="first_name = 'John'\nlast_name = 'Doe'\nphone_number = '555-1234'"
            ),
            VimGolfProblem(
                id="9v0066dd4c36",
                title="Markdown Blog Editing", 
                description="Convert link text to markdown link format",
                start_text="Visit our website at https://example.com for more info.\nCheck out https://github.com/user/repo for the code.",
                end_text="Visit our website at [https://example.com](https://example.com) for more info.\nCheck out [https://github.com/user/repo](https://github.com/user/repo) for the code."
            ),
            VimGolfProblem(
                id="9v0066cbb6a1",
                title="Remove adjacent duplicates",
                description="Remove consecutive repeated characters",
                start_text="aabbccddee\nhhellooo wwoorlld",
                end_text="abcde\nhelo world"
            ),
            VimGolfProblem(
                id="9v0066daede5",
                title="Word completion",
                description="Complete abbreviated words with full versions",
                start_text="func main() {\n    var msg str = \"Hello\"\n    fmt.Println(msg)\n}",
                end_text="function main() {\n    var message string = \"Hello\"\n    fmt.Println(message)\n}"
            )
        ]
    
    def create_prompt(self, problem: VimGolfProblem) -> str:
        """Create a detailed prompt for the LLM to solve a VimGolf problem"""
        return f"""You are a Vim expert solving a VimGolf challenge. Your goal is to transform the START text into the END text using the minimum number of Vim keystrokes.

PROBLEM: {problem.title}
DESCRIPTION: {problem.description}
PROBLEM ID: {problem.id}

START TEXT:
```
{problem.start_text}
```

END TEXT:
```
{problem.end_text}
```

INSTRUCTIONS:
1. Assume you start in normal mode with cursor at position 1,1 (beginning of file)
2. Provide the exact sequence of Vim keystrokes needed
3. Use standard Vim notation (e.g., <Esc>, <CR> for Enter, <C-a> for Ctrl+A)
4. Aim for the minimum number of keystrokes possible
5. Explain your solution step by step
6. Count the total keystrokes in your solution

RESPONSE FORMAT:
Solution: [your vim keystroke sequence]
Keystrokes: [total count]
Explanation: [step by step breakdown]

Remember: Every character counts in VimGolf! Be as efficient as possible."""

    def solve_problem(self, problem: VimGolfProblem) -> Dict:
        """Solve a single VimGolf problem using OpenAI"""
        prompt = self.create_prompt(problem)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a Vim expert who excels at solving VimGolf challenges with minimal keystrokes."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=1000
            )
            
            return {
                "problem_id": problem.id,
                "title": problem.title,
                "solution": response.choices[0].message.content,
                "success": True
            }
            
        except Exception as e:
            return {
                "problem_id": problem.id, 
                "title": problem.title,
                "error": str(e),
                "success": False
            }
    
    def solve_all_problems(self) -> List[Dict]:
        """Solve all 10 VimGolf problems"""
        results = []
        
        print("🏌️ VimGolf Solver - Solving 10 curated challenges...\n")
        
        for i, problem in enumerate(self.problems, 1):
            print(f"[{i}/10] Solving: {problem.title}")
            print(f"Description: {problem.description}")
            print("=" * 60)
            
            result = self.solve_problem(problem)
            results.append(result)
            
            if result["success"]:
                print("✅ Solution generated!")
                print(result["solution"])
            else:
                print(f"❌ Error: {result['error']}")
            
            print("\n" + "=" * 60 + "\n")
        
        return results
    
    def print_summary(self, results: List[Dict]):
        """Print a summary of all solutions"""
        successful = [r for r in results if r["success"]]
        failed = [r for r in results if not r["success"]]
        
        print(f"\n📊 SUMMARY")
        print(f"Successfully solved: {len(successful)}/10 problems")
        print(f"Failed: {len(failed)}/10 problems")
        
        if failed:
            print(f"\nFailed problems:")
            for result in failed:
                print(f"- {result['title']}: {result['error']}")


def main():
    """Main entry point"""
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("Please set your OpenAI API key:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        sys.exit(1)
    
    solver = VimGolfSolver()
    results = solver.solve_all_problems()
    solver.print_summary(results)


if __name__ == "__main__":
    main()