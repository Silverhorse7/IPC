import gradio as gr
import os
import google.generativeai as genai
# # Configure the Google Generative AI with the API key from the environment variable
GOOGLE_API_KEY = os.environ['GEMINI_KEY']
genai.configure(api_key=GOOGLE_API_KEY)

# Define the detailed summarization system prompt
summarization_system_prompt = """
You are an AI assistant that specializes in extracting the core problem from competitive programming problem statements. Your goal is to identify and present only the essential problem that needs to be solved, removing all extra information.
When given a problem statement, follow these steps:
1. Read the problem statement carefully to understand the underlying task.
2. Identify the core problem that needs to be solved, ignoring all unnecessary details.
3. Remove the following from the problem statement:
    - Any background stories, characters, or flavor text
    - Explanations of the problem or its motivation
    - Examples demonstrating the problem or its solution
    - Specific input/output formats or constraints
    - Scoring information or test case details
    - Any LaTeX or other formatting syntax
4. Rephrase the core problem concisely in your own words, using as few words as possible while still preserving clarity.
5. Avoid using any jargon, symbols, extra explanations, or formulas.
6. Present the core problem directly, without any additional context or commentary.
7. Review your extracted core problem to ensure it is a complete, standalone statement of the task to be solved, adhering to the steps above.
Your output should be a single, concise statement of the core problem, without any extra information or explanation. The goal is to provide a clear, unambiguous problem statement that captures the essence of the problem, and nothing more.
"""

# Initialize the generative model and start a chat session with the system prompt
summarization_model = genai.GenerativeModel('gemini-1.5-flash')
summarization_chat = summarization_model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [summarization_system_prompt],
    },
    {
      "role": "model",
      "parts": [
        "Okay, I'm ready to extract the core problems from your competitive programming problem statements. Just provide me with the full problem statement, and I'll analyze it and give you the most concise version of the problem to solve.",
      ],
    },
  ]
)


# Define the function to perform summarization
def perform_summarization(text):
    response = summarization_chat.send_message(text)
    return response.text


# Another model for a different functionality, e.g., code generation
code_gen_prompt = "Provide a code snippet for the following description:"

# Initialize another generative model for code generation
code_gen_model = genai.GenerativeModel('gemini-1.5-flash')
code_gen_chat = code_gen_model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [code_gen_prompt],
    },
    {
      "role": "model",
      "parts": [
        "I'm ready to generate code snippets based on your descriptions. Please provide the description.",
      ],
    },
  ]
)

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
persist_directory = "db"


model = genai.GenerativeModel('gemini-1.5-flash')

chat = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "## Intelligent Programming Companion (IPC): System Prompt\n\nYou are the Intelligent Programming Companion (IPC), a sophisticated AI specializing in competitive programming and C++.  Your primary goal is to guide users in solving coding problems by providing clear explanations, efficient C++ solutions, and insightful analysis. \n\n**Core Functionality:**\n\n1. **Problem Identification:**  Carefully analyze user messages to determine if they contain a programming problem requiring a solution. Look for keywords like \"solve,\" \"code,\" \"algorithm,\" problem descriptions, or code snippets.  \n\n2. **Relevance Filtering (Using Provided Data):**\n    * You will be provided with the user's message AND a set of relevant problems and C++ solutions retrieved from a dataset based on the user's query.\n    *  Even if a problem is identified, the provided data may not always be relevant (e.g., the user might be asking a clarifying question or discussing a concept). \n    * Analyze this provided data and ONLY use it if it directly relates to the user's current problem. \n\n3. **Solution Generation and Analysis:** If the user has presented a problem AND the provided data is relevant:\n    * **Understand the Problem:**  Thoroughly analyze the problem statement to identify the core task, constraints, and desired input/output.\n    * **Craft a C++ Solution:** Develop an efficient and well-structured C++ solution that addresses all aspects of the problem.\n    * **Explain the Approach:** Provide a clear and concise explanation of the chosen algorithm, data structures, and logic behind your solution. Use code comments within the solution for clarity.\n    * **Analyze Complexity:** Determine and explain the time complexity (Big O notation) and space complexity of your solution, highlighting its efficiency.\n\n4. **General Guidance and Best Practices:**\n    * If the provided data is not relevant, offer general guidance, insights into related programming concepts, or suggest potential approaches.\n    * Share best practices for competitive programming, including tips on code optimization, avoiding common pitfalls, and choosing the right data structures.\n\n**Communication Style:**\n\n* **Empathetic and Encouraging:**  Maintain a positive and encouraging tone, fostering a supportive learning environment. \n* **Patient and Clear:** Explain concepts thoroughly, using simple language and avoiding technical jargon. Break down complex ideas into smaller, more digestible parts.\n* **Professional and Concise:**  Your responses should be well-structured, grammatically correct, and easy to understand.\n\n**Remember:**\n\n* Your primary goal is to guide and educate users, empowering them to solve problems independently. \n* Focus on providing clear explanations, efficient code, and valuable insights into problem-solving techniques.\n\n**Example Interaction:**\n\n**User Prompt:**  \"Hi IPC! Can you help me write a C++ program to find the shortest path between two nodes in a weighted graph? I was thinking of using Dijkstra's algorithm.\"\n\n**Relevant Problems and Solutions:** [This section will contain the retrieved data (potentially including Dijkstra's algorithm implementations) that you need to analyze for relevance]. \n\nPrint Yes to confirm you understand and will follow that system prompt.",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Yes \n",
      ],
    },
  ]
)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
retriever = db.as_retriever(search_kwargs={"k": 5})
def get_relevant_context(query):
    docs = retriever.invoke(query)
    context = "\n".join([doc.page_content for doc in docs])
    return context

def predict(message, history):
    relevant_context = get_relevant_context(message)
    modified_user_prompt = "USER ORIGINAL MESSAGE:\n" + message
    modified_user_prompt += "\n\n\n------------------------------------------------------------------------------------------------------------------------\n\n\n"
    modified_user_prompt += "ADDED SECTION OF MAYBE-RELEVANT PROBLEMS WITH SOLUTIONS. IGNORE IF THE ORIGINAL USER MESSAGE ISN'T ASKING ABOUT A PROBLEM:\n"
    modified_user_prompt += relevant_context

    response = chat.send_message(modified_user_prompt)
    return response.text


import requests

# The API endpoint URL
url = 'http://34.166.48.42:5555/difficulty'  # Replace with your actual API endpoint
similarity_problem = 'http://34.166.48.42:5555/similarity_problem'
similarity_solution = 'http://34.166.48.42:5555/similarity_solution'
def inference(problem_statement):
    # The JSON object to send (with one key-value pair)
    data = {'problem': problem_statement}
    # Send the POST request with the JSON data
    response = requests.post(url, json=data)
    if response.status_code == 200:
        pred = response.json()
        return ", ".join(pred['tags']), str(pred['rating'])
    else:
        return response.text, response.text
    
glob = {}

import json
import random
import string
import math

def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def generate_random_json_object():
    return {
        "problem_link": f"https://example.com/problem/{generate_random_string()}",
        "solution": generate_random_string(20),
        "similarity": round(random.uniform(0, 1), 2)
    }

def get_similar_problems(problem_statement, problem_solution, top_k):
    if not problem_statement:
        if not problem_solution:
            return "ERROR: Input the problem's statement and/or solution"
        # The JSON object to send (with one key-value pair)
        data = {'solution': problem_solution,
                'top_k': top_k}
        # Send the POST request with the JSON data
        response = requests.post(similarity_solution, json=data)
        if response.status_code == 200:
            similar_solutions = response.json()
        # similar_solutions = [generate_random_json_object() for _ in range(10)]
            ret = {}
            glob.clear()
            for json_obj in similar_solutions:
                problem_link = json_obj.get("problem_link", "No problem link provided")
                if isinstance(problem_link, float) and math.isnan(problem_link):
                  problem_link = "No problem link provided"
                ret[problem_link] = float(json_obj.get("similarity", "0%").replace('%', ''))/100
                glob[problem_link] = json_obj.get("solution", "No problem solution provided")
            return ret
        else:
            glob.clear()
            return {"NaN" : 0}
    else:
        # The JSON object to send (with one key-value pair)
        data = {'problem': problem_statement,
                'top_k': top_k}
        # Send the POST request with the JSON data
        response = requests.post(similarity_problem, json=data)
        if response.status_code == 200:
            similar_problems = response.json()
            ret = {}
            glob.clear()
            for json_obj in similar_problems:
                problem_link = json_obj.get("problem_link", "No problem link provided")
                if isinstance(problem_link, float) and math.isnan(problem_link):
                  problem_link = "No problem link provided"
                ret[problem_link] = float(json_obj.get("similarity", "0%").replace('%', ''))/100
                glob[problem_link] = json_obj.get("problem_statement", "No problem statement provided")
            return ret
        else:
            glob.clear()
            return {"NaN" : 0}
        
def show_problem(evt: gr.SelectData):  # SelectData is a subclass of EventData
    uid = evt.value
    if uid != "NaN":
        statement = glob[uid]
        title = uid 
        url = uid
        markdown = f"# [{title}]({url})\n\n"
        markdown += f"### Statement\n\n{statement}"
        return markdown

with gr.Blocks(title="IPC Intelligent Programming Companion", css=".mymarkdown {font-size: 15px !important}") as demo:
    gr.Markdown(
        """
    # IPC Intelligent Programming Companion
    Your Gateway to Competitive Programming and Interview Preparation
    """
    )
    with gr.Tabs():
        with gr.TabItem("Summarization"):
            problem = gr.Textbox(label="Problem Statement")
            summary_output = gr.Textbox(label="Summary")
            summarize_btn = gr.Button("Summarize")
            summarize_btn.click(fn=perform_summarization, inputs=problem, outputs=summary_output)

        with gr.TabItem("Solver"):
            gr.ChatInterface(predict).launch

        with gr.TabItem("Difficulty"):
            problem = gr.Textbox(label="Problem Statement")
            tags = gr.Textbox(label="Tags")
            difficulty = gr.Textbox(label="Difficulty")
            predict_btn = gr.Button("Predict")
            predict_btn.click(fn=inference, inputs=problem, outputs=[tags,difficulty])
        with gr.TabItem("Similarity"):
            with gr.Row():
              # column for inputs
              with gr.Column():
                problem_statement = gr.Textbox(
                    label="Statement",
                    info="Paste your statement here!",
                    value=""
                )
                problem_solution = gr.Textbox(
                    label="Solution",
                    info="Paste your solution here!",
                    value=""
                )
                topk_slider = gr.Slider(
                    minimum=1,
                    maximum=100,
                    step=1,
                    value=10,
                    label="Number of similar problems to show",
                )
                submit_button = gr.Button("Submit")
                my_markdown = gr.Markdown(
                    latex_delimiters=[
                        {"left": "$$", "right": "$$", "display": True},
                        {"left": "$", "right": "$", "display": False},
                        {"left": "\\(", "right": "\\)", "display": False},
                        {"left": "\\[", "right": "\\]", "display": True},
                    ],
                    elem_classes="mymarkdown",
                )
              # column for outputs
              with gr.Column():
                  output_labels = gr.Label(
                      label="Similar problems"
                  )
            submit_button.click(
                fn=get_similar_problems,
                inputs=[problem_statement, problem_solution, topk_slider],
                outputs=[output_labels],
            )
            output_labels.select(fn=show_problem, inputs=None, outputs=[my_markdown])



# Launch the Gradio interface
demo.launch(share=True)