import os

def detect_bugs(code_lines):
    """Simple bug detector - checks for common issues"""
    issues = []
    for i, line in enumerate(code_lines, 1):
        if 'print(' in line and '#' not in line:
            issues.append(f"Line {i}: Consider using logging instead of print()")
        if line.strip().endswith('==') or line.strip().endswith('='):
            issues.append(f"Line {i}: Possible incomplete comparison/assignment")
        if 'except:' in line:
            issues.append(f"Line {i}: Bare except clause - specify exception type")
    return issues


def check_style(code_lines):
    """Simple style checker - checks formatting conventions"""
    issues = []
    for i, line in enumerate(code_lines, 1):
        if len(line) > 79:
            issues.append(f"Line {i}: Line too long ({len(line)} chars, max 79)")
        if line != line.rstrip() and line.strip() != '':
            issues.append(f"Line {i}: Trailing whitespace")
        if '\t' in line:
            issues.append(f"Line {i}: Use spaces instead of tabs")
    return issues


def orchestrator(file_path):
    """Main orchestrator - reads file and delegates to agents"""
    print(f"\n{'='*50}")
    print(f"  Code Review Agent System")
    print(f"  Reviewing: {file_path}")
    print(f"{'='*50}\n")

    with open(file_path, 'r') as f:
        code_lines = f.readlines()

    print("Agent 1 (Bug Detector) analyzing...")
    bug_issues = detect_bugs(code_lines)

    print("Agent 2 (Style Checker) analyzing...\n")
    style_issues = check_style(code_lines)

    print("--- BUG DETECTOR REPORT ---")
    if bug_issues:
        for issue in bug_issues:
            print(f"  ⚠️  {issue}")
    else:
        print("  ✅ No bugs detected!")

    print("\n--- STYLE CHECKER REPORT ---")
    if style_issues:
        for issue in style_issues:
            print(f"  ⚠️  {issue}")
    else:
        print("  ✅ No style issues!")

    print(f"\n{'='*50}")
    total = len(bug_issues) + len(style_issues)
    print(f"  Total issues found: {total}")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    orchestrator("sample_code.py")