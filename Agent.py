import json
import os
import platform
import subprocess
from dataclasses import dataclass
from typing import Any, Dict, Optional
from pathlib import Path

import ollama


MODEL_NAME = "qwen3.5"
MAX_STEPS = 10
MAX_TOOL_OUTPUT_CHARS = 12000
SHELL_TIMEOUT_SECONDS = 8
PYTHON_TIMEOUT_SECONDS = 5

WORKSPACE_DIR = Path(r"C:\Users\AISW_203_121\Desktop\agent").resolve()

class AgentError(Exception):
    pass


class ToolValidationError(AgentError):
    pass


class ToolExecutionError(AgentError):
    pass


def ensure_workspace_dir() -> Path:
    WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
    return WORKSPACE_DIR


def resolve_workspace_path(path_str: str) -> Path:
    workspace = ensure_workspace_dir()
    path = Path(os.path.expandvars(path_str))

    if path.is_absolute():
        resolved = path.resolve()
    else:
        resolved = (workspace / path).resolve()

    try:
        resolved.relative_to(workspace)
    except ValueError:
        raise ToolExecutionError(f"Access outside workspace is not allowed: {resolved}")

    return resolved


def truncate(text: str, limit: int = MAX_TOOL_OUTPUT_CHARS) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + "\n\n...[truncated]..."


def safe_json_loads(text: str) -> Dict[str, Any]:
    text = text.strip()

    if text.startswith("```"):
        lines = text.splitlines()
        if len(lines) >= 3:
            text = "\n".join(lines[1:-1]).strip()

    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise AgentError(f"Model returned invalid JSON: {e}\nRaw output:\n{text}")

    if not isinstance(data, dict):
        raise AgentError("Model output must be a JSON object.")
    return data


def run_shell(command: str) -> str:
    command = os.path.expandvars(command).strip()

    blocked_patterns = [
        "python -c",
        "python3 -c",
        "py -c",
        "powershell -encodedcommand",
        "rm -rf /",
        "del /f /s /q",
        "format ",
    ]
    lowered = command.lower()
    for pattern in blocked_patterns:
        if pattern in lowered:
            raise ToolExecutionError(f"Blocked command pattern detected: {pattern}")

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=SHELL_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        raise ToolExecutionError(f"Command timed out after {SHELL_TIMEOUT_SECONDS} seconds.")
    except Exception as e:
        raise ToolExecutionError(f"Shell execution failed: {e}")

    stdout = result.stdout.strip()
    stderr = result.stderr.strip()

    if stdout and stderr:
        return f"[stdout]\n{stdout}\n\n[stderr]\n{stderr}"
    if stdout:
        return stdout
    if stderr:
        return stderr
    return "[no output]"


def read_file(path: str) -> str:
    resolved_path = resolve_workspace_path(path)

    if not resolved_path.exists():
        raise ToolExecutionError(f"File not found: {resolved_path}")
    if not resolved_path.is_file():
        raise ToolExecutionError(f"Path is not a file: {resolved_path}")

    encodings = ["utf-8", "cp949", "euc-kr"]
    errors = []

    for encoding in encodings:
        try:
            with open(resolved_path, "r", encoding=encoding) as f:
                return f.read()
        except Exception as e:
            errors.append(f"{encoding}: {e}")

    raise ToolExecutionError(
        "Unable to read the file with supported encodings.\n" + "\n".join(errors)
    )


def read_docx(path: str) -> str:
    resolved_path = resolve_workspace_path(path)

    if not resolved_path.exists():
        raise ToolExecutionError(f"File not found: {resolved_path}")
    if not resolved_path.is_file():
        raise ToolExecutionError(f"Path is not a file: {resolved_path}")

    try:
        from docx import Document
    except ImportError:
        raise ToolExecutionError("python-docx is not installed. Run: pip install python-docx")

    try:
        doc = Document(resolved_path)
        paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        text = "\n".join(paragraphs)
        return text if text else "Document is empty or has no readable paragraphs."
    except Exception as e:
        raise ToolExecutionError(f"Error reading docx: {e}")


def run_python(code: str) -> str:
    if not isinstance(code, str) or not code.strip():
        raise ToolValidationError("run_python requires a non-empty string field: code")

    banned_patterns = [
        "import os",
        "from os",
        "import sys",
        "from sys",
        "import subprocess",
        "from subprocess",
        "import pathlib",
        "from pathlib",
        "import shutil",
        "from shutil",
        "import socket",
        "from socket",
        "import builtins",
        "from builtins",
        "import ctypes",
        "from ctypes",
        "import importlib",
        "from importlib",
        "__import__(",
        "open(",
        "eval(",
        "exec(",
    ]

    lowered = code.lower()
    for pattern in banned_patterns:
        if pattern in lowered:
            raise ToolExecutionError(f"Blocked Python pattern detected: {pattern}")

    workspace = ensure_workspace_dir()

    try:
        result = subprocess.run(
            ["python", "-I", "-c", code],
            capture_output=True,
            text=True,
            timeout=PYTHON_TIMEOUT_SECONDS,
            cwd=str(workspace),
        )
    except subprocess.TimeoutExpired:
        raise ToolExecutionError(
            f"Python code timed out after {PYTHON_TIMEOUT_SECONDS} seconds."
        )
    except Exception as e:
        raise ToolExecutionError(f"Python execution failed: {e}")

    stdout = result.stdout.strip()
    stderr = result.stderr.strip()

    if stdout and stderr:
        return f"[stdout]\n{stdout}\n\n[stderr]\n{stderr}"
    if stdout:
        return stdout
    if stderr:
        return stderr
    return "[no output]"

def run_tool(tool_name: str, arguments: Dict[str, Any]) -> str:
    if tool_name == "run_shell":
        command = arguments.get("command")
        if not isinstance(command, str) or not command.strip():
            raise ToolValidationError("run_shell requires a non-empty string field: command")
        return run_shell(command)

    if tool_name == "read_file":
        path = arguments.get("path")
        if not isinstance(path, str) or not path.strip():
            raise ToolValidationError("read_file requires a non-empty string field: path")
        return read_file(path)

    if tool_name == "read_docx":
        path = arguments.get("path")
        if not isinstance(path, str) or not path.strip():
            raise ToolValidationError("read_docx requires a non-empty string field: path")
        return read_docx(path)

    if tool_name == "run_python":
        code = arguments.get("code")
        if not isinstance(code, str) or not code.strip():
            raise ToolValidationError("run_python requires a non-empty string field: code")
        return run_python(code)

    raise ToolValidationError(f"Unknown tool: {tool_name}")
# =========================================================
# Agent Response Schema
# =========================================================
@dataclass
class ToolCall:
    tool: str
    arguments: Dict[str, Any]


@dataclass
class AgentDecision:
    reasoning: Optional[str]
    final_answer: Optional[str]
    tool_call: Optional[ToolCall]
    done: bool

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "AgentDecision":
        reasoning = data.get("reasoning")
        final_answer = data.get("final_answer")
        tool_call_raw = data.get("tool_call")
        done = data.get("done")

        if reasoning is not None and not isinstance(reasoning, str):
            raise AgentError("'reasoning' must be a string or null.")
        if final_answer is not None and not isinstance(final_answer, str):
            raise AgentError("'final_answer' must be a string or null.")
        if not isinstance(done, bool):
            raise AgentError("'done' must be a boolean.")

        tool_call = None
        if tool_call_raw is not None:
            if not isinstance(tool_call_raw, dict):
                raise AgentError("'tool_call' must be an object or null.")
            tool = tool_call_raw.get("tool")
            arguments = tool_call_raw.get("arguments")

            if not isinstance(tool, str) or not tool.strip():
                raise AgentError("'tool_call.tool' must be a non-empty string.")
            if not isinstance(arguments, dict):
                raise AgentError("'tool_call.arguments' must be an object.")

            tool_call = ToolCall(tool=tool, arguments=arguments)

        if done:
            if final_answer is None:
                raise AgentError("When done=true, 'final_answer' must not be null.")
            if tool_call is not None:
                raise AgentError("When done=true, 'tool_call' must be null.")
        else:
            if tool_call is None:
                raise AgentError("When done=false, 'tool_call' must not be null.")

        return AgentDecision(
            reasoning=reasoning,
            final_answer=final_answer,
            tool_call=tool_call,
            done=done,
        )


# =========================================================
# Prompt
# =========================================================
SYSTEM_PROMPT = f"""
You are a tool-using assistant.

You must respond with EXACTLY ONE JSON object, and nothing else.

Available tools:
1. run_shell
   arguments: {{"command": "shell command string"}}

2. read_file
   arguments: {{"path": "path to a text file"}}

3. read_docx
   arguments: {{"path": "path to a .docx file"}}

4. run_python
   arguments: {{"code": "short Python code for safe computation or text processing"}}

Rules:
- Never invent tool results.
- Use tools whenever real-world file or system inspection is needed.
- Do NOT use python -c or inline scripts through run_shell.
- Use run_shell ONLY when:
  - you need system info
  - you need file listing
- Use run_python ONLY when:
  - you need calculation
  - you need text processing
  - you need simple data transformation
- Do NOT use run_python for file access or system commands.
- If the task is complete, return done=true and provide final_answer.
- If the task is not complete, return done=false and provide exactly one tool_call.
- Do not output markdown, code fences, XML tags, or extra commentary.

JSON schema:
{{
  "reasoning": "optional short reasoning string or null",
  "done": true,
  "final_answer": "string when done=true",
  "tool_call": null
}}

or

{{
  "reasoning": "optional short reasoning string or null",
  "done": false,
  "final_answer": null,
  "tool_call": {{
    "tool": "run_shell | read_file | read_docx | run_python",
    "arguments": {{}}
  }}
}}

Current OS: {platform.system()}
""".strip()


# =========================================================
# Pretty Printing
# =========================================================
def print_banner(step: int) -> None:
    print(f"\n{'=' * 48}")
    print(f"Step {step}")
    print(f"{'=' * 48}")


def print_reasoning(reasoning: Optional[str]) -> None:
    if reasoning:
        print("\n[Reasoning]")
        print(reasoning)


def print_tool_call(tool_call: ToolCall) -> None:
    print("\n[Tool Call]")
    print(json.dumps(
        {"tool": tool_call.tool, "arguments": tool_call.arguments},
        indent=2,
        ensure_ascii=False
    ))


def print_tool_result(result: str) -> None:
    print("\n[Tool Result]")
    print(result)


def print_final_answer(answer: str) -> None:
    print("\n[Final Answer]")
    print(answer)


# =========================================================
# Agent Core
# =========================================================
def agent_loop(user_input: str) -> None:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input},
    ]

    for step in range(1, MAX_STEPS + 1):
        print_banner(step)

        try:
            response = ollama.chat(model=MODEL_NAME, messages=messages)
            raw_reply = response.message.content.strip()

            data = safe_json_loads(raw_reply)
            decision = AgentDecision.from_dict(data)

            print_reasoning(decision.reasoning)

            if decision.done:
                print_final_answer(decision.final_answer or "")
                print("\n[Agent Completed Successfully]")
                return

            assert decision.tool_call is not None
            print_tool_call(decision.tool_call)

            try:
                tool_result = run_tool(decision.tool_call.tool, decision.tool_call.arguments)
            except (ToolValidationError, ToolExecutionError) as e:
                tool_result = f"TOOL_ERROR: {e}"

            tool_result = truncate(tool_result)
            print_tool_result(tool_result)

            messages.append({"role": "assistant", "content": raw_reply})
            messages.append({
                "role": "user",
                "content": (
                    "Tool result:\n"
                    f"{tool_result}\n\n"
                    "Continue. If the task is complete, return done=true with final_answer. "
                    "Otherwise return the next tool_call."
                )
            })

        except AgentError as e:
            print(f"\n[Agent Error]\n{e}")
            messages.append({
                "role": "user",
                "content": (
                    f"Your previous response was invalid.\n{e}\n\n"
                    "Return exactly one valid JSON object matching the required schema."
                )
            })
        except Exception as e:
            print(f"\n[Fatal Error]\n{e}")
            return

    print("\n[Stopped: max steps reached]")


# =========================================================
# Entry Point
# =========================================================
if __name__ == "__main__":
    user_query = input("Enter your request:\n> ")
    agent_loop(user_query)
