import ast
import argparse

def get_lowest_index(a, b):
    if a == -1 and b == -1:
        return -1
    elif a == -1:
        return b
    elif b == -1:
        return a
    else:
        return min(a, b)

def extract_docstrings(file_path):
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())
    
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    docstrings = {}
    
    for func in functions:
        docstring = ast.get_docstring(func)
        if docstring:
            docstrings[func.name] = docstring
    
    return docstrings

def format_for_markdown(docstrings):
    markdown = "## Functions Documentation\n\n"
    for func_name, docstring in docstrings.items():
        markdown += f"### `{func_name}`\n\n"
        args_index = docstring.find("Args")
        returns_index = docstring.find("Returns")
        description_end_index = get_lowest_index(args_index, returns_index)
        markdown += f"{docstring[:description_end_index].strip()}\n\n"
        
        if args_index != -1 :
            arguments = docstring[args_index:returns_index].split("\n")
            markdown += f"\n**Args:**\n\n"
            for arg in arguments[1:]:
                arg = arg.strip()
                if arg:
                    narg = arg.split(":")
                    if len(narg) == 1:
                        markdown += f" - **{narg[0]}** \n"
                    else:
                        markdown += f" - **{narg[0]}**: {narg[1]} \n"
            markdown += "\n"

        if returns_index != -1:
            returns = docstring[returns_index:-1].split("\n")
            markdown += f"**Returns:**\n"
            for ret in returns[1:]:
                ret = ret.strip()
                if ret:
                    markdown += f" - {ret}\n"   
            markdown += "\n"   

        markdown += "\n"
    return markdown

def main():
    parser = argparse.ArgumentParser(description="Extract docstrings from a Python script and append them to a README file.")
    parser.add_argument('script_file', help="The Python script file to extract docstrings from.")
    parser.add_argument('readme_file', help="The README file to append the documentation to.")
    
    args = parser.parse_args()

    docstrings = extract_docstrings(args.script_file)
    markdown = format_for_markdown(docstrings)
    
    if args.readme_file:
        with open(args.readme_file, 'a') as readme:
            readme.write(markdown)
    else:
        print(markdown)

if __name__ == "__main__":
    main()