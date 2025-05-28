import ast
from collections import defaultdict
import argparse

# Skip these built-ins and user-defined functions
BUILTIN_EXCLUDE = {"print", "len", "range", "int", "str", "float", "input", "open"}
EXCLUDE_FUNCTIONS = {"timed" }  # Your own functions to ignore

class FunctionCallVisitor(ast.NodeVisitor):
    def __init__(self):
        self.function_calls = defaultdict(list)
        self.current_function = None
        self.defined_functions = set()
        self.function_docs = {}  # to include the docstring

    def visit_FunctionDef(self, node):
        if node.name in EXCLUDE_FUNCTIONS:
            return  # Skip this function entirely
        self.defined_functions.add(node.name)
        docstring = ast.get_docstring(node)
        self.function_docs[node.name] = docstring  # <--- Store docstring
        prev_function = self.current_function
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = prev_function

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if (
                self.current_function
                and func_name not in BUILTIN_EXCLUDE
                and func_name not in EXCLUDE_FUNCTIONS
            ):
                self.function_calls[self.current_function].append(func_name)
        self.generic_visit(node)

def build_call_tree(filename):
    with open(filename, 'r') as f:
        tree = ast.parse(f.read(), filename)

    visitor = FunctionCallVisitor()
    visitor.visit(tree)

    # Filter out unwanted calls from the final tree
    filtered_calls = {
        func: [callee for callee in callees if callee in visitor.defined_functions]
        for func, callees in visitor.function_calls.items()
        if func not in EXCLUDE_FUNCTIONS
    }

    return filtered_calls


def print_call_tree(call_map, function_docs, start=None, prefix='', visited=None, is_last=True):
    if visited is None:
        visited = set()

    if start is None:
        # Detect roots
        called = {callee for callees in call_map.values() for callee in callees}
        roots = [f for f in call_map.keys() if f not in called]
        for i, root in enumerate(roots):
            is_last_root = (i == len(roots) - 1)
            print_call_tree(call_map, function_docs, start=root, prefix='', visited=visited, is_last=is_last_root)
        return

    BLUE = "\033[34m"
    ITALIC = "\033[3m"
    RESET = "\033[0m"
    # Print the current function with the right prefix
    connector = '└── ' if is_last else '├── '
    doc = function_docs.get(start)
    doc_part = f' | {ITALIC}{BLUE}{doc.strip()}{RESET}' if doc else ''
    print(f"{prefix}{connector}{start}(){doc_part}" if prefix else f"{start}(){doc_part}")

    if start in visited:
        return
    visited.add(start)

    # Prepare child prefix
    children = call_map.get(start, [])
    new_prefix = prefix + ('    ' if is_last else '│   ')

    for i, child in enumerate(children):
        is_last_child = (i == len(children) - 1)
        print_call_tree(call_map, function_docs, child, new_prefix, visited, is_last_child)


def usage():
    """ usage() function """
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Specify a Python script filename')
    #parser.add_argument('-v', action='store_true', help='verbose output')
    return parser.parse_args()


# Example usage
if __name__ == "__main__":

    args = usage()
    filename = args.filename
    print(f'\033[3m\033[34m#{filename = }:\033[0m')

    visitor = FunctionCallVisitor()
    with open(filename) as f:
        tree = ast.parse(f.read(), filename)
        visitor.visit(tree)

    call_map = {
        func: [callee for callee in callees if callee in visitor.defined_functions]
        for func, callees in visitor.function_calls.items()
        if func not in EXCLUDE_FUNCTIONS
    }

    print_call_tree(call_map, visitor.function_docs)

