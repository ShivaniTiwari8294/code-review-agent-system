import os
import glob

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLOR = True
except ImportError:
    COLOR = False
    class Fore:
        RED = YELLOW = GREEN = CYAN = MAGENTA = ""
    class Style:
        RESET_ALL = ""


def detect_bugs(code_lines):
    """Agent 1: Bug Detector"""
    issues = []
    for i, line in enumerate(code_lines, 1):
        if 'print(' in line and '#' not in line:
            issues.append((f"Line {i}: Consider using logging instead of print()",
                            "Replace print() with logging.info()"))
        if line.strip().endswith('==') or line.strip().endswith('='):
            issues.append((f"Line {i}: Possible incomplete comparison/assignment",
                            "Complete the expression"))
        if 'except:' in line:
            issues.append((f"Line {i}: Bare except clause - specify exception type",
                            "Use 'except SpecificError:' instead"))
    return issues


def check_style(code_lines):
    """Agent 2: Style Checker"""
    issues = []
    for i, line in enumerate(code_lines, 1):
        if len(line) > 79:
            issues.append((f"Line {i}: Line too long ({len(line)} chars, max 79)",
                            "Break into multiple lines"))
        if line != line.rstrip() and line.strip() != '':
            issues.append((f"Line {i}: Trailing whitespace",
                            "Remove trailing spaces"))
        if '\t' in line:
            issues.append((f"Line {i}: Use spaces instead of tabs",
                            "Replace tabs with 4 spaces"))
    return issues


def check_performance(code_lines):
    """Agent 3: Performance Agent"""
    issues = []
    nested_loop_depth = 0
    for i, line in enumerate(code_lines, 1):
        stripped = line.strip()
        if stripped.startswith('for ') or stripped.startswith('while '):
            indent = len(line) - len(line.lstrip())
            if indent > 0:
                issues.append((f"Line {i}: Nested loop detected - check for O(n^2) complexity",
                                "Consider using a dictionary/set for lookups"))
        if '.append(' in line and 'for' in ''.join(code_lines[max(0, i-3):i]):
            issues.append((f"Line {i}: Loop with .append() - consider list comprehension",
                            "Use: result = [x for x in items]"))
        if 'range(len(' in line:
            issues.append((f"Line {i}: 'range(len())' pattern - use enumerate() instead",
                            "Use: for i, item in enumerate(items)"))
    return issues


def calculate_score(total_issues, total_lines):
    """Calculate code quality score out of 10"""
    if total_lines == 0:
        return 10
    ratio = total_issues / total_lines
    score = max(0, 10 - (ratio * 20))
    return round(score, 1)


def print_report(title, issues, color):
    print(f"\n{color}--- {title} ---{Style.RESET_ALL}")
    if issues:
        for issue, fix in issues:
            print(f"  {color}⚠️  {issue}{Style.RESET_ALL}")
            print(f"     💡 Fix: {fix}")
    else:
        print(f"  {Fore.GREEN}✅ No issues found!{Style.RESET_ALL}")


def review_file(file_path):
    """Orchestrator: reviews a single file using all agents"""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"  📄 Reviewing: {file_path}")
    print(f"{'='*60}{Style.RESET_ALL}")

    with open(file_path, 'r') as f:
        code_lines = f.readlines()

    bug_issues = detect_bugs(code_lines)
    style_issues = check_style(code_lines)
    perf_issues = check_performance(code_lines)

    print_report("BUG DETECTOR AGENT", bug_issues, Fore.RED)
    print_report("STYLE CHECKER AGENT", style_issues, Fore.YELLOW)
    print_report("PERFORMANCE AGENT", perf_issues, Fore.MAGENTA)

    total = len(bug_issues) + len(style_issues) + len(perf_issues)
    score = calculate_score(total, len(code_lines))

    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"  Total issues: {total}")
    print(f"  Code Quality Score: {score}/10")
    print(f"{'='*60}{Style.RESET_ALL}\n")

    return total, score


def orchestrator(target):
    """Main orchestrator - handles single file or directory"""
    print(f"\n{Fore.CYAN}🤖 ORCHESTRATOR: Starting Code Review System{Style.RESET_ALL}")

    if os.path.isdir(target):
        py_files = glob.glob(os.path.join(target, "*.py"))
        py_files = [f for f in py_files if 'orchestrator' not in f]
    else:
        py_files = [target]

    if not py_files:
        print(f"{Fore.RED}No Python files found!{Style.RESET_ALL}")
        return

    print(f"🤖 ORCHESTRATOR: Found {len(py_files)} file(s) to review")
    print(f"🤖 ORCHESTRATOR: Delegating to Bug Detector, Style Checker, and Performance agents...\n")

    results = {}
    for file_path in py_files:
        total, score = review_file(file_path)
        results[file_path] = score

    print(f"{Fore.CYAN}{'='*60}")
    print(f"  📊 SUMMARY")
    print(f"{'='*60}{Style.RESET_ALL}")
    for file_path, score in results.items():
        print(f"  {file_path}: {score}/10")


if __name__ == "__main__":
    orchestrator("sample_code.py")