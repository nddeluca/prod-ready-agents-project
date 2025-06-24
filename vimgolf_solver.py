#!/usr/bin/env python3
"""
VimGolf Problem Solver using OpenAI

This script presents 10 curated VimGolf challenges to an LLM and asks it to solve them
by generating the minimal Vim command sequences needed to transform the input text.
"""

import os
import sys
import re
import asyncio
import time
import logging
from typing import Dict, List, Tuple
from dataclasses import dataclass
from openai import AsyncOpenAI
from src.pynvim_agents.raw_editor import RawNvimEditor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)


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
        self.client = AsyncOpenAI(api_key=api_key or os.getenv('OPENAI_API_KEY'))
        self.problems = self._load_problems()
        self.logger = logging.getLogger(__name__)
    
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

    def extract_solution_from_response(self, response_text: str) -> str:
        """Extract the vim keystroke sequence from LLM response"""
        # Look for "Solution:" followed by the keystroke sequence on the same line
        solution_match = re.search(r'Solution:\s*([^\n]+)', response_text)
        if solution_match:
            candidate = solution_match.group(1).strip()
            # Skip if it's just code block markers
            if candidate in ['```', '```vim', '```viml']:
                pass  # Continue to other extraction methods
            else:
                candidate = self._clean_backticks(candidate)
                if candidate and self._looks_like_vim_command(candidate):
                    return candidate
        
        # Look for content in code blocks
        code_block_match = re.search(r'```(?:vim|viml)?\n([^`]+)\n```', response_text, re.MULTILINE)
        if code_block_match:
            candidate = code_block_match.group(1).strip()
            if candidate and self._looks_like_vim_command(candidate):
                return candidate
        
        # Look for content between single backticks (not code blocks)
        # Match single-line backtick content only
        backtick_match = re.search(r'`([^`\n]+)`', response_text)
        if backtick_match:
            candidate = backtick_match.group(1).strip()
            if candidate and self._looks_like_vim_command(candidate):
                return candidate
                
        # Look for lines that start with vim command patterns
        lines = response_text.split('\n')
        for line in lines:
            line = line.strip()
            # Skip empty lines and code block markers
            if not line or line.startswith('```'):
                continue
            # Remove surrounding backticks if present
            line = self._clean_backticks(line)
            if line and self._looks_like_vim_command(line):
                return line
                
        return ""
    
    def _clean_backticks(self, text: str) -> str:
        """Remove surrounding backticks from text"""
        text = text.strip()
        if text.startswith('`') and text.endswith('`'):
            return text[1:-1].strip()
        return text
    
    def _looks_like_vim_command(self, text: str) -> bool:
        """Check if text looks like a vim command sequence"""
        if not text:
            return False
            
        # Skip descriptive text
        if any(text.lower().startswith(phrase) for phrase in [
            'the vim keystrokes are:', 'i would use', 'here\'s', 'this will',
            'explanation:', 'keystrokes:', 'step', 'first', 'then', 'next'
        ]):
            return False
            
        # Check for vim command patterns
        vim_patterns = [
            r'^:',           # Ex commands (:s, :g, etc)
            r'^[0-9]*[a-zA-Z]',  # Normal mode commands (dd, yy, etc)
            r'<[A-Z][a-z]*>',    # Special keys (<Esc>, <CR>, etc)
            r'[ijaoIO]',         # Insert mode commands
            r'[/?]',             # Search commands
            r'[\'"`]',           # Marks, registers
        ]
        
        return any(re.search(pattern, text) for pattern in vim_patterns)
    
    def count_keystrokes(self, keystroke_sequence: str) -> int:
        """
        Count the number of actual keystrokes in a vim command sequence.
        This accounts for special key notations like <CR>, <Esc>, etc.
        """
        if not keystroke_sequence:
            return 0
            
        # Replace special key sequences with single characters for counting
        # Common vim special keys
        special_keys = [
            '<CR>', '<Enter>', '<Return>',  # Enter key
            '<Esc>', '<Escape>',            # Escape key  
            '<Tab>', '<S-Tab>',             # Tab keys
            '<BS>', '<Backspace>',          # Backspace
            '<Del>', '<Delete>',            # Delete
            '<Up>', '<Down>', '<Left>', '<Right>',  # Arrow keys
            '<C-[a-zA-Z]>', '<C-[0-9]>',    # Ctrl combinations
            '<S-[a-zA-Z]>',                 # Shift combinations
            '<A-[a-zA-Z]>',                 # Alt combinations
            '<F[0-9]+>',                    # Function keys
            '<Home>', '<End>',              # Home/End
            '<PageUp>', '<PageDown>',       # Page navigation
            '<Insert>',                     # Insert key
        ]
        
        # Count the sequence
        temp_sequence = keystroke_sequence
        keystroke_count = 0
        
        # Handle special key patterns
        special_key_patterns = [
            r'<CR>|<Enter>|<Return>',
            r'<Esc>|<Escape>',
            r'<Tab>|<S-Tab>',
            r'<BS>|<Backspace>',
            r'<Del>|<Delete>',
            r'<Up>|<Down>|<Left>|<Right>',
            r'<C-[a-zA-Z0-9]>',
            r'<S-[a-zA-Z]>',
            r'<A-[a-zA-Z]>',
            r'<F[0-9]+>',
            r'<Home>|<End>',
            r'<PageUp>|<PageDown>',
            r'<Insert>'
        ]
        
        # Replace each special key pattern with a placeholder and count
        for pattern in special_key_patterns:
            matches = re.findall(pattern, temp_sequence, re.IGNORECASE)
            keystroke_count += len(matches)
            temp_sequence = re.sub(pattern, '', temp_sequence, flags=re.IGNORECASE)
        
        # Count remaining regular characters
        keystroke_count += len(temp_sequence)
        
        return keystroke_count

    async def evaluate_solution(self, problem: VimGolfProblem, keystroke_sequence: str) -> int:
        """
        Evaluate a solution by executing it in nvim and checking if result matches expected output.
        Returns 1 if buffer matches expected output, 0 otherwise.
        """
        try:
            # Skip evaluation if no keystrokes
            if not keystroke_sequence or not keystroke_sequence.strip():
                return 0
                
            # Prepare initial content as list of lines
            start_lines = problem.start_text.split('\n')
            expected_lines = problem.end_text.split('\n')
            
            # Run nvim evaluation in executor with timeout
            loop = asyncio.get_event_loop()
            result = await asyncio.wait_for(
                loop.run_in_executor(None, self._run_nvim_evaluation, start_lines, expected_lines, keystroke_sequence),
                timeout=5.0  # 5 second timeout per evaluation
            )
            return result
                
        except asyncio.TimeoutError:
            self.logger.warning(f"⏱️ Evaluation timeout for: {problem.title}")
            return 0
        except Exception as e:
            self.logger.warning(f"⚠️ Evaluation error for {problem.title}: {str(e)}")
            return 0
    
    def _run_nvim_evaluation(self, start_lines: List[str], expected_lines: List[str], keystroke_sequence: str) -> int:
        """Helper method to run nvim evaluation synchronously"""
        try:
            with RawNvimEditor(initial_content=start_lines) as editor:
                # Set vim to suppress error messages and continue on errors
                editor.nvim.command("set shortmess+=IacF") # Suppress various messages
                editor.nvim.command("set noerrorbells")    # No error bells
                editor.nvim.command("set visualbell t_vb=") # No visual bell
                editor.nvim.command("set report=999")       # Don't report changes
                editor.nvim.command("set noswapfile")       # Disable swap files
                editor.nvim.command("set nobackup")         # Disable backup files
                editor.nvim.command("set nowritebackup")    # Disable write backup
                
                # Execute the keystroke sequence with error handling
                try:
                    editor.type_keys(keystroke_sequence)
                except Exception:
                    # If keystroke execution fails, try to continue
                    pass
                
                # Ensure we're in normal mode before getting content
                try:
                    editor.type_keys("<Esc>")
                except Exception:
                    pass
                
                # Get the resulting buffer content
                result_lines = editor.get_buffer_content()
                
                # Compare with expected output
                # Remove any trailing empty lines for comparison
                result_lines_clean = [line for line in result_lines if line.strip()]
                expected_lines_clean = [line for line in expected_lines if line.strip()]
                
                # Also try exact match including empty lines
                while result_lines and result_lines[-1] == '':
                    result_lines.pop()
                while expected_lines and expected_lines[-1] == '':
                    expected_lines.pop()
                
                # Return 1 if either exact match or content match (ignoring empty lines)
                exact_match = result_lines == expected_lines
                content_match = result_lines_clean == expected_lines_clean
                
                return 1 if (exact_match or content_match) else 0
                
        except Exception:
            return 0

    async def solve_problem(self, problem: VimGolfProblem) -> Dict:
        """Solve a single VimGolf problem using OpenAI and evaluate the solution"""
        start_time = time.time()
        self.logger.info(f"🔄 Starting problem: {problem.title}")
        
        prompt = self.create_prompt(problem)
        
        try:
            # OpenAI API call
            api_start = time.time()
            self.logger.info(f"🤖 Calling OpenAI API for: {problem.title}")
            
            response = await self.client.chat.completions.create(
                model="gpt-4.1",
                messages=[
                    {"role": "system", "content": "You are a Vim expert who excels at solving VimGolf challenges with minimal keystrokes."},
                    {"role": "user", "content": prompt}
                ],
            )
            
            api_time = time.time() - api_start
            self.logger.info(f"✅ OpenAI response received for: {problem.title} ({api_time:.1f}s)")
            
            response_text = response.choices[0].message.content
            keystroke_sequence = self.extract_solution_from_response(response_text)
            self.logger.info(f"🔍 Extracted keystrokes: {keystroke_sequence}")
            
            # Count keystrokes
            keystroke_count = self.count_keystrokes(keystroke_sequence) if keystroke_sequence else 0
            
            # Evaluate the solution
            eval_start = time.time()
            self.logger.info(f"🧪 Evaluating solution in vim environment...")
            eval_score = await self.evaluate_solution(problem, keystroke_sequence) if keystroke_sequence else 0
            eval_time = time.time() - eval_start
            
            total_time = time.time() - start_time
            status = "✅ PASS" if eval_score == 1 else "❌ FAIL"
            self.logger.info(f"{status} {problem.title} - Score: {eval_score}, Keystrokes: {keystroke_count}, Eval: {eval_time:.1f}s, Total: {total_time:.1f}s")
            
            return {
                "problem_id": problem.id,
                "title": problem.title,
                "solution": response_text,
                "keystroke_sequence": keystroke_sequence,
                "keystroke_count": keystroke_count,
                "eval_score": eval_score,
                "api_time": api_time,
                "eval_time": eval_time,
                "total_time": total_time,
                "success": True
            }
            
        except Exception as e:
            total_time = time.time() - start_time
            self.logger.error(f"❌ ERROR {problem.title}: {str(e)} ({total_time:.1f}s)")
            return {
                "problem_id": problem.id, 
                "title": problem.title,
                "error": str(e),
                "eval_score": 0,
                "keystroke_count": 0,
                "total_time": total_time,
                "success": False
            }
    
    async def solve_all_problems(self) -> List[Dict]:
        """Solve all 10 VimGolf problems concurrently"""
        total_start = time.time()
        self.logger.info("🏌️  VimGolf Solver - Starting 10 concurrent challenges")
        self.logger.info("🚀 Launching all API calls simultaneously...")
        
        # Create tasks for all problems to run concurrently
        tasks = [self.solve_problem(problem) for problem in self.problems]
        
        # Execute all tasks concurrently with progress updates
        results = await asyncio.gather(*tasks)
        
        total_time = time.time() - total_start
        self.logger.info(f"🏁 All problems completed in {total_time:.1f}s")
        
        # Print detailed results
        print("\n" + "="*80)
        print("🎯 DETAILED RESULTS")
        print("="*80)
        
        for i, (problem, result) in enumerate(zip(self.problems, results), 1):
            print(f"\n[{i}/10] {problem.title}")
            print(f"Description: {problem.description}")
            print("-" * 60)
            
            if result["success"]:
                eval_score = result.get("eval_score", 0)
                status_icon = "✅" if eval_score == 1 else "❌"
                api_time = result.get("api_time", 0)
                eval_time = result.get("eval_time", 0)
                total_time = result.get("total_time", 0)
                keystroke_count = result.get("keystroke_count", 0)
                
                print(f"{status_icon} Score: {eval_score} | Keystrokes: {keystroke_count} | API: {api_time:.1f}s | Eval: {eval_time:.1f}s | Total: {total_time:.1f}s")
                if "keystroke_sequence" in result:
                    print(f"Command: {result['keystroke_sequence']}")
                print("\nLLM Response:")
                print(result["solution"][:300] + "..." if len(result["solution"]) > 300 else result["solution"])
            else:
                total_time = result.get("total_time", 0)
                print(f"❌ Error ({total_time:.1f}s): {result['error']}")
        
        return results
    
    def print_summary(self, results: List[Dict]):
        """Print a summary of all solutions"""
        successful = [r for r in results if r["success"]]
        failed = [r for r in results if not r["success"]]
        correct_solutions = [r for r in results if r.get("eval_score", 0) == 1]
        
        # Calculate timing stats
        total_api_time = sum(r.get("api_time", 0) for r in successful)
        total_eval_time = sum(r.get("eval_time", 0) for r in successful)
        avg_api_time = total_api_time / len(successful) if successful else 0
        avg_eval_time = total_eval_time / len(successful) if successful else 0
        
        # Calculate keystroke stats
        total_keystrokes = sum(r.get("keystroke_count", 0) for r in successful)
        avg_keystrokes = total_keystrokes / len(successful) if successful else 0
        correct_keystrokes = sum(r.get("keystroke_count", 0) for r in correct_solutions)
        
        print(f"\n📊 PERFORMANCE SUMMARY")
        print("="*50)
        print(f"✅ Successfully solved: {len(successful)}/10 problems")
        print(f"🎯 Correctly solved (eval_score = 1): {len(correct_solutions)}/10 problems")
        print(f"❌ Failed: {len(failed)}/10 problems")
        print(f"⏱️  Average API time: {avg_api_time:.1f}s")
        print(f"🧪 Average eval time: {avg_eval_time:.1f}s")
        print(f"⌨️  Total keystrokes: {total_keystrokes}")
        print(f"📊 Average keystrokes per problem: {avg_keystrokes:.1f}")
        print(f"🎯 Keystrokes in correct solutions: {correct_keystrokes}")
        print(f"🔢 Success rate: {len(correct_solutions)/10*100:.1f}%")
        
        if failed:
            print(f"\n❌ Failed problems:")
            for result in failed:
                print(f"   • {result['title']}: {result['error']}")
                
        if successful:
            print(f"\n🎯 Problem breakdown:")
            for result in successful:
                eval_score = result.get("eval_score", 0)
                keystroke_count = result.get("keystroke_count", 0)
                status = "✅" if eval_score == 1 else "❌"
                print(f"   {status} {result['title']}: Score {eval_score} | {keystroke_count} keystrokes")


async def main():
    """Main entry point"""
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("Please set your OpenAI API key:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        sys.exit(1)
    
    solver = VimGolfSolver()
    try:
        results = await solver.solve_all_problems()
        solver.print_summary(results)
    finally:
        # Close the OpenAI client
        try:
            await solver.client.close()
        except Exception:
            pass


if __name__ == "__main__":
    asyncio.run(main())
