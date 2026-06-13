import os
import glob
import re

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class Fore:
        RED = YELLOW = GREEN = CYAN = MAGENTA = BLUE = ""
    class Style:
        RESET_ALL = ""


# ============ UNIVERSAL CHECKS (all languages) ============

def check_universal_style(code_lines):
    """Agent 2: Style Checker - works for all languages"""
    issues = []
    for i, line in enumerate(code_lines, 1):
        if len(line) > 100:
            issues.append((f"Line {i}: Line too long ({len(line)} chars, max 100)",
                            "Break into multiple lines"))
        if line != line.rstrip() and line.strip() != '':
            issues.append((f"Line {i}: Trailing whitespace",
                            "Remove trailing spaces"))
        if '\t' in line:
            issues.append((f"Line {i}: Use spaces instead of tabs",
                            "Replace tabs with spaces"))
        if 'TODO' in line or 'FIXME' in line:
            issues.append((f"Line {i}: Unresolved TODO/FIXME comment",
                            "Resolve or track this in an issue tracker"))
    return issues


def check_universal_security(code_lines):
    """Agent 4: Security Agent - works for all languages"""
    issues = []
    secret_patterns = [
        (r'password\s*[=:]\s*["\'].+["\']', "Hardcoded password detected"),
        (r'api_key\s*[=:]\s*["\'].+["\']', "Hardcoded API key detected"),
        (r'secret\s*[=:]\s*["\'].+["\']', "Hardcoded secret detected"),
        (r'token\s*[=:]\s*["\'].+["\']', "Hardcoded token detected"),
    ]
    for i, line in enumerate(code_lines, 1):
        lower_line = line.lower()
        for pattern, msg in secret_patterns:
            if re.search(pattern, lower_line):
                issues.append((f"Line {i}: {msg}",
                                "Use environment variables / config files instead"))
        if 'eval(' in line:
            issues.append((f"Line {i}: Use of eval() is dangerous",
                            "Avoid eval(); use safer alternatives"))
    return issues


# ============ PYTHON-SPECIFIC CHECKS ============

def check_python_bugs(code_lines):
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


def check_python_performance(code_lines):
    issues = []
    for i, line in enumerate(code_lines, 1):
        stripped = line.strip()
        if (stripped.startswith('for ') or stripped.startswith('while ')) and (len(line) - len(line.lstrip())) > 0:
            issues.append((f"Line {i}: Nested loop detected - check for O(n^2) complexity",
                            "Consider using a dictionary/set for lookups"))
        if 'range(len(' in line:
            issues.append((f"Line {i}: 'range(len())' pattern - use enumerate() instead",
                            "Use: for i, item in enumerate(items)"))
    return issues


def check_python_docs(code_lines):
    issues = []
    for i, line in enumerate(code_lines):
        stripped = line.strip()
        if stripped.startswith('def '):
            next_line = code_lines[i+1].strip() if i+1 < len(code_lines) else ""
            if not (next_line.startswith('"""') or next_line.startswith("'''")):
                func_name = stripped.split('(')[0].replace('def ', '')
                issues.append((f"Line {i+1}: Function '{func_name}' missing docstring",
                                "Add a docstring describing what the function does"))
    return issues


# ============ JAVASCRIPT-SPECIFIC CHECKS ============

def check_js_bugs(code_lines):
    issues = []
    for i, line in enumerate(code_lines, 1):
        if re.search(r'\bvar\b', line):
            issues.append((f"Line {i}: 'var' usage detected",
                            "Use 'let' or 'const' instead of 'var'"))
        if re.search(r'[^=!<>]==[^=]', line):
            issues.append((f"Line {i}: Loose equality '==' used",
                            "Use strict equality '===' instead"))
        if 'console.log(' in line:
            issues.append((f"Line {i}: console.log() left in code",
                            "Remove debug console.log statements"))
    return issues


def check_js_docs(code_lines):
    issues = []
    for i, line in enumerate(code_lines):
        stripped = line.strip()
        if re.match(r'(function\s+\w+|const\s+\w+\s*=\s*\(.*\)\s*=>)', stripped):
            prev_line = code_lines[i-1].strip() if i > 0 else ""
            if not prev_line.endswith('*/') and '//' not in prev_line:
                issues.append((f"Line {i+1}: Function missing comment/JSDoc",
                                "Add a comment describing the function"))
    return issues


# ============ JAVA-SPECIFIC CHECKS ============

def check_java_bugs(code_lines):
    issues = []
    for i, line in enumerate(code_lines, 1):
        if 'System.out.println' in line:
            issues.append((f"Line {i}: System.out.println() found",
                            "Use a logging framework (e.g., SLF4J) instead"))
        stripped = line.strip()
        if re.match(r'(public|private|protected)?\s*(static\s+)?(void|int|String|boolean|double)\s+\w+\(', stripped):
            if not re.match(r'(public|private|protected)', stripped):
                issues.append((f"Line {i}: Method missing access modifier",
                                "Add 'public', 'private', or 'protected'"))
    return issues


# ============ C/C++-SPECIFIC CHECKS ============

def check_cpp_bugs(code_lines):
    issues = []
    for i, line in enumerate(code_lines, 1):
        if 'using namespace std;' in line:
            issues.append((f"Line {i}: 'using namespace std' found",
                            "Avoid in larger projects; use std:: prefix instead"))
        if re.search(r'\bgoto\b', line):
            issues.append((f"Line {i}: 'goto' statement used",
                            "Avoid goto; use loops/functions for control flow"))
        if re.search(r'\bmalloc\(', line) and 'free(' not in ''.join(code_lines):
            issues.append((f"Line {i}: malloc() used without matching free()",
                            "Ensure every malloc() has a corresponding free()"))
    return issues


# ============ LANGUAGE DETECTION ============

LANGUAGE_MAP = {
    '.py': 'Python',
    '.js': 'JavaScript',
    '.java': 'Java',
    '.cpp': 'C++',
    '.c': 'C',
    '.h': 'C/C++ Header',
}


def get_language(file_path):
    ext = os.path.splitext(file_path)[1]
    return LANGUAGE_MAP.get(ext, 'Unknown')


def run_language_specific_checks(file_path, code_lines):
    """Agent 1 (bugs) and Agent 5 (docs) - language aware"""
    ext = os.path.splitext(file_path)[1]
    bug_issues = []
    doc_issues = []

    if ext == '.py':
        bug_issues = check_python_bugs(code_lines)
        doc_issues = check_python_docs(code_lines)
    elif ext == '.js':
        bug_issues = check_js_bugs(code_lines)
        doc_issues = check_js_docs(code_lines)
    elif ext == '.java':
        bug_issues = check_java_bugs(code_lines)
    elif ext in ('.cpp', '.c', '.h'):
        bug_issues = check_cpp_bugs(code_lines)

    return bug_issues, doc_issues


def run_performance_checks(file_path, code_lines):
    """Agent 3 - language aware"""
    ext = os.path.splitext(file_path)[1]
    if ext == '.py':
        return check_python_performance(code_lines)
    return []


# ============ SCORING & REPORTING ============

def calculate_score(total_issues, total_lines):
    """Score based on error percentage: every 10% error rate reduces score by 1"""
    if total_lines == 0:
        return 10
    error_percentage = (total_issues / total_lines) * 100
    penalty = error_percentage / 10
    score = 10 - penalty
    score = max(0, min(10, score))
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
    language = get_language(file_path)
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"  📄 Reviewing: {file_path}  [{language}]")
    print(f"{'='*60}{Style.RESET_ALL}")

    if language == 'Unknown':
        print(f"  {Fore.YELLOW}⚠️  Unsupported file type - skipping detailed checks{Style.RESET_ALL}")
        return 0, 10

    with open(file_path, 'r') as f:
        code_lines = f.readlines()

    bug_issues, doc_issues = run_language_specific_checks(file_path, code_lines)
    style_issues = check_universal_style(code_lines)
    perf_issues = run_performance_checks(file_path, code_lines)
    security_issues = check_universal_security(code_lines)

    print_report("BUG DETECTOR AGENT", bug_issues, Fore.RED)
    print_report("STYLE CHECKER AGENT", style_issues, Fore.YELLOW)
    print_report("PERFORMANCE AGENT", perf_issues, Fore.MAGENTA)
    print_report("SECURITY AGENT", security_issues, Fore.BLUE)
    print_report("DOCUMENTATION AGENT", doc_issues, Fore.CYAN)

    total = (len(bug_issues) + len(style_issues) + len(perf_issues)
             + len(security_issues) + len(doc_issues))
    score = calculate_score(total, len(code_lines))

    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"  Total issues: {total}")
    print(f"  Code Quality Score: {score}/10")
    print(f"{'='*60}{Style.RESET_ALL}\n")

    return {
        "file": file_path,
        "language": language,
        "bugs": bug_issues,
        "style": style_issues,
        "performance": perf_issues,
        "security": security_issues,
        "documentation": doc_issues,
        "total_issues": total,
        "score": score
    }

    return total, score


def orchestrator(target):
    print(f"\n{Fore.CYAN}🤖 ORCHESTRATOR: Starting Multi-Language Code Review System{Style.RESET_ALL}")

    supported_exts = tuple(LANGUAGE_MAP.keys())

    if os.path.isdir(target):
        all_files = []
        for ext in supported_exts:
            all_files.extend(glob.glob(os.path.join(target, f"*{ext}")))
        py_files = [f for f in all_files if 'orchestrator' not in f]
    else:
        py_files = [target]

    if not py_files:
        print(f"{Fore.RED}No supported files found!{Style.RESET_ALL}")
        return

    print(f"🤖 ORCHESTRATOR: Found {len(py_files)} file(s) to review")
    print(f"🤖 ORCHESTRATOR: Delegating to 5 specialized agents "
          f"(Bug, Style, Performance, Security, Documentation)...\n")

    results = {}
    for file_path in py_files:
       data = review_file(file_path)
       results[file_path] = (data["score"], data["language"])

    print(f"{Fore.CYAN}{'='*60}")
    print(f"  📊 SUMMARY")
    print(f"{'='*60}{Style.RESET_ALL}")
    for file_path, (score, lang) in results.items():
        print(f"  {file_path} [{lang}]: {score}/10")


if __name__ == "__main__":
    orchestrator(".")