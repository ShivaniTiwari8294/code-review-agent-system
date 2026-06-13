# Code Review Agent System

An AI-inspired orchestration system that automatically reviews Python code using specialized agents.

## How It Works

The **Orchestrator** reads a Python file and delegates analysis to two specialized agents:

- **Bug Detector Agent** — Identifies common issues like bare except clauses, incomplete comparisons, and debug print statements
- **Style Checker Agent** — Checks for PEP8 violations like long lines, trailing whitespace, and tab usage

## Usage# code-review-agent-systemPlace your code in `sample_code.py` and run the orchestrator to get a full review report.

## Inspiration

Built using the **Agent Orchestration** pattern — where a central orchestrator agent coordinates specialized sub-agents to complete complex tasks, similar to a project manager directing a team.

## Future Scope

- Integrate with GitHub Copilot CLI for AI-powered suggestions
- Add a Performance Agent to detect inefficient code
- Auto-fix detected issues
- GitHub Actions integration for automatic PR reviews
@@new features............
## Agents

1. **Bug Detector Agent** — Finds bare excepts, incomplete expressions, debug prints
2. **Style Checker Agent** — PEP8 violations (line length, whitespace, tabs)
3. **Performance Agent** — Detects nested loops, inefficient patterns

## Code Quality Score

Each file gets a score out of 10 based on issue density. Lower score = more issues relative to file size.