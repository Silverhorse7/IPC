import pandas as pd
import re
from pygments.lexers import CppLexer
from pygments.token import Token
import os
import tempfile
import subprocess
import xml.etree.ElementTree as ET

def remove_comments(code):
    # Remove single line & multi-line comments
    regex = '\/\/.*|\/\*(\S|\s)*\*\/'
    code = re.sub(regex, '', code)
    return code

def remove_include_directives_namespace(code):
    # Remove the include directives
    code = re.sub(r'#include.*', '', code)
    # Remove the using namespace
    code = re.sub(r'using namespace.*', '', code)
    return code

def remove_non_ascii(code):
    return code.encode('ascii', 'ignore').decode('ascii')

def clean_code(code):
    if code:
        return code.replace('\n', ' ').replace('\r', ' ')

# def replace_macros(id, code):
#     if code is None:
#         return None
#     # Create a temp directory
#     TMP_DIR = tempfile.mkdtemp()

#     # Open a new file in a temp directory and write the source code into it
#     with open(os.path.join(TMP_DIR, f'temp_{id}.cpp'), 'w') as file:
#         file.write(code)

#     # Run the preprocessor
#     preprocessed_file_path = os.path.join(TMP_DIR, f'temp_preprocessed_{id}.cpp')
#     command = f"g++ -E -P {os.path.join(TMP_DIR, f'temp_{id}.cpp')} -o {preprocessed_file_path}"
#     try:
#         subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
#     except subprocess.CalledProcessError as e:
#         print(f"Preprocessing failed for id {id}:", e.output.decode())
#         return None

#     # Read the preprocessed code
#     try:
#         with open(preprocessed_file_path, 'r') as file:
#             preprocessed_code = file.read()
#     except FileNotFoundError:
#         print(f"Preprocessed file not found for id {id}.")
#         return None

#     # Remove the temp files
#     os.remove(os.path.join(TMP_DIR, f'temp_{id}.cpp'))
#     os.remove(preprocessed_file_path)
#     os.rmdir(TMP_DIR)

#     return preprocessed_code

def removing_unused_functions(id, code):
    # Create a temp directory
    TMP_DIR = tempfile.mkdtemp()

    # Open a new file in a temp directory and write the source code into it
    with open(os.path.join(TMP_DIR, f'temp_{id}.cpp'), 'w') as file:
        file.write(code)

    # Performs static code analysis and outputs the results in an XML file
    try:
        os.system(
            f"cppcheck --enable=all --xml -q --output-file=\"{os.path.join(TMP_DIR, f'temp_{id}.xml')}\" {os.path.join(TMP_DIR, f'temp_{id}.cpp')}")
    except Exception as e:
        print(
            f"Error occurred during cppcheck execution for id {id}: {str(e)}")
        return None

    # Parse the XML file
    try:
        tree = ET.parse(os.path.join(TMP_DIR, f'temp_{id}.xml'))
        root = tree.getroot()
    except Exception as e:
        print(f"Error occurred during XML parsing for id {id}: {str(e)}")
        return None

    lines = code.split("\n")
    errors = root.find("errors")
    remove_lines = set()

    if not errors:
        preprocessed_code = "\n".join(lines)
        # Remove the temp files
        os.remove(os.path.join(TMP_DIR, f'temp_{id}.cpp'))
        os.remove(os.path.join(TMP_DIR, f'temp_{id}.xml'))
        os.rmdir(TMP_DIR)
        return preprocessed_code

    for error in errors.findall("error"):
        if error.get("id") == "unusedFunction":
            location = int(error.find('location').get('line')) - 1
            count_ph = 0
            seen_the_end = False
            index = location

            for line in lines[location:]:
                remove_lines.add(index)
                index += 1
                for ch in line:
                    if ch == "{":
                        count_ph += 1
                    elif ch == "}":
                        count_ph -= 1
                        seen_the_end = True

                if count_ph == 0 and seen_the_end:
                    break

    lines = [line for idx, line in enumerate(lines)
             if idx not in remove_lines and len(line) > 0]

    preprocessed_code = "\n".join(lines)

    # Remove the temp files
    os.remove(os.path.join(TMP_DIR, f'temp_{id}.cpp'))
    os.remove(os.path.join(TMP_DIR, f'temp_{id}.xml'))
    os.rmdir(TMP_DIR)

    return preprocessed_code

# def generate_assembly(id, code):
#     # Create a temp directory
#     TMP_DIR = tempfile.mkdtemp()

#     # Open a new file in a temp directory and write the source code into it
#     with open(os.path.join(TMP_DIR, f'temp_{id}.cpp'), 'w') as file:
#         file.write(code)

#     # Compile the code
#     try:
#         os.system(
#             f"g++ -S {os.path.join(TMP_DIR, f'temp_{id}.cpp')} -o {os.path.join(TMP_DIR, f'temp_{id}.s')}")
#     except Exception as e:
#         print(
#             f"Error occurred during generating assembly code for id {id}: {str(e)}")

#     # Read the assembly code
#     try:
#         with open(os.path.join(TMP_DIR, f'temp_{id}.s'), 'r') as file:
#             assembly_code = file.read()
#     except FileNotFoundError:
#         print(f"Assembly file not found for id {id}.")
#         return None

#     # Remove the temp files
#     os.remove(os.path.join(TMP_DIR, f'temp_{id}.cpp'))
#     os.remove(os.path.join(TMP_DIR, f'temp_{id}.s'))
#     os.rmdir(TMP_DIR)

#     return assembly_code

# Tokenize C++ code
def tokenize(code):
    if code is None:
        return None
    tokens = []
    for token_type, value in CppLexer().get_tokens(code):
        if token_type in Token.Literal or token_type in Token.Name or token_type in Token.Keyword or token_type in Token.Operator:
            tokens.append(value)
    return tokens

# Define a function to preprocess a batch of solutions
def preprocess_batch(batch):
    preprocessed_solutions = []
    # assembly_solutions = []
    tokenized_solutions = []
    for _, row in batch.iterrows():
        id = row['index']
        code = row['solution']
        code = remove_comments(code)
        code = remove_non_ascii(code)
        code = remove_include_directives_namespace(code)
        code = removing_unused_functions(id, code)
        # code = replace_macros(id, code)
        tokenized_code = tokenize(code)
        code = clean_code(code)
        preprocessed_solutions.append(code)
        tokenized_solutions.append(tokenized_code)
    return preprocessed_solutions, tokenized_solutions

# Define a function to apply batch processing to the entire dataset
def preprocess_dataset(df, batch_size=100):
    preprocessed_solutions = []
    tokenized_solutions = []
    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i+batch_size]
        preprocessed_batch, tokenized_batch = preprocess_batch(batch)
        preprocessed_solutions.extend(preprocessed_batch)
        tokenized_solutions.extend(tokenized_batch)
        print(f"Processed {i + len(batch)} out of {len(df)}")
    return preprocessed_solutions, tokenized_solutions