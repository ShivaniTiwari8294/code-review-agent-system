# 🤖 AI Multi-Agent Code Review System

A web-based orchestration platform where a central orchestrator delegates code analysis to 5 specialized AI agents — inspired by the Agent Orchestration pattern.

## Features

- **Multi-language support**: Python, JavaScript, Java, C/C++
- **Multi-file upload**: Add files cumulatively, review all at once
- **5 Specialized Agents**:
  - 🐛 Bug Detector Agent
  - 🎨 Style Checker Agent
  - ⚡ Performance Agent
  - 🔒 Security Agent
  - 📝 Documentation Agent
- **Section-wise view**: Browse issues by category across all files
- **Code Quality Scoring**: 0-10 score based on issue density
- **Built-in Chat Assistant**: Ask about any detected issue and get explanations

## How It Works

The **Orchestrator** receives uploaded files, detects their language, and delegates analysis to each specialized agent. Results are aggregated into a score and displayed in an organized dashboard.

## Tech Stack

- Python, Flask (backend)
- HTML/CSS/JavaScript (frontend)
- Regex-based static analysis engine

## Usage Open the forwarded port (5000) in your browser, upload code files, and click "Review All Files".

## Future Scope

- Real GitHub Copilot AI integration for deeper suggestions
- GitHub Actions integration for automatic PR reviews
- Auto-fix application
- Support for more languages (Go, Rust, TypeScript)## 🎥 Demo Video

## 🎥 Demo Video

[Download and watch the demo video](My%20Movie%201.mp4)

