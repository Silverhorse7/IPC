import nbformat

def update_inference_parameter(notebook_path, new_parameter):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    code_cell_index = 0  
    new_code = f"problem_statement = \"{new_parameter}\""
    nb['cells'][code_cell_index]['source'] = new_code

    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)