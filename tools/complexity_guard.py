#!/usr/bin/env python3
"""Cheap AST review heuristic; does not prove algorithmic time complexity."""
import argparse
import ast
import json
from pathlib import Path

BRANCH_NODES = (ast.If, ast.IfExp, ast.For, ast.AsyncFor, ast.While, ast.ExceptHandler,
                ast.With, ast.AsyncWith, ast.Match, ast.Try)
NESTING_NODES = (ast.If, ast.For, ast.AsyncFor, ast.While, ast.Match, ast.Try)


def function_metrics(source: str, filename: str = '<memory>') -> list[dict]:
    tree = ast.parse(source, filename=filename)
    results = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        score = 1
        max_nesting = 0
        # Don't count nested functions/classes as part of the outer body.
        def visit(current: ast.AST, nesting: int = 0):
            nonlocal score, max_nesting
            for child in ast.iter_child_nodes(current):
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
                    continue
                next_depth = nesting + int(isinstance(child, NESTING_NODES))
                if isinstance(child, BRANCH_NODES):
                    score += 1 + min(nesting, 5)
                if isinstance(child, ast.BoolOp):
                    score += max(0, len(child.values) - 1)
                max_nesting = max(max_nesting, next_depth)
                visit(child, next_depth)
        visit(node)
        results.append({'file': filename, 'function': node.name, 'line': node.lineno,
                        'score': score, 'max_nesting': max_nesting,
                        'async': isinstance(node, ast.AsyncFunctionDef)})
    return results


def analyze(paths: list[str]) -> list[dict]:
    result = []
    for name in paths:
        file = Path(name)
        if not file.is_file() or file.suffix != '.py':
            raise ValueError(f'Not a readable Python file: {name}')
        result.extend(function_metrics(file.read_text(encoding='utf-8'), str(file)))
    return sorted(result, key=lambda x: (-x['score'], x['file'], x['line']))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('files', nargs='+')
    parser.add_argument('--max-score', type=int, default=30)
    args = parser.parse_args()
    if args.max_score < 1:
        parser.error('--max-score must be positive')
    try:
        items = analyze(args.files)
    except (ValueError, SyntaxError, OSError, UnicodeError) as exc:
        parser.error(str(exc))
    flagged = [x for x in items if x['score'] > args.max_score]
    print(json.dumps({'metric': 'syntactic-branching-heuristic', 'functions': items,
                      'threshold': args.max_score, 'flagged': len(flagged)}, indent=2))
    return 1 if flagged else 0

if __name__ == '__main__':
    raise SystemExit(main())
