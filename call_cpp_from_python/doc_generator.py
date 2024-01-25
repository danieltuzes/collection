import inspect
import call_cpp_from_python


def get_function_signature_and_docstring(func):
    # Get the full docstring
    full_docstring = inspect.getdoc(func)
    if not full_docstring:
        return "(...) -> Any", "    \"\"\"Docstring not available\"\"\""

    # Split the docstring into lines
    lines = full_docstring.split('\n')

    # The first line is the signature
    signature_line = lines[0] if lines else ""

    # Find the start of the parameter list and extract the substring
    param_start = signature_line.find('(')
    if param_start != -1:
        signature = signature_line[param_start:]
    else:
        signature = signature_line  # Fallback

    # Format the rest of the docstring
    docstring_lines = lines[1:]  # All lines except the signature line
    formatted_docstring = "    \"\"\"" + \
        "\n    ".join([line.strip()
                      for line in docstring_lines if line.strip()]) + "\"\"\""
    return signature, formatted_docstring


# Module docstring
module_docstring = inspect.getdoc(
    call_cpp_from_python) or "Module docstring not available"

# Start writing the .pyi file
with open('call_cpp_from_python.pyi', 'w') as f:
    # Write the header and the module docstring
    f.write('"""' + module_docstring + '"""\n\n')
    f.write('from typing import List, Any\n\n')

    # Get all the callables in the module
    for name, obj in inspect.getmembers(call_cpp_from_python):
        if inspect.isfunction(obj) or inspect.isbuiltin(obj):
            signature, docstring = get_function_signature_and_docstring(obj)
            f.write(f"def {name}{signature}:\n{docstring}\n    ...\n\n")
