import gradio as gr
# from mistralai.client import MistralClient
# from mistralai.models.chat_completion import ChatMessage
import os 
import google.generativeai as genai

GOOGLE_API_KEY = os.environ['GEMINI_KEY']
genai.configure(api_key=GOOGLE_API_KEY)

# mixtral_api_key = os.environ['MIXTRAL_API_KEY']
# mixtral_model = "open-mixtral-8x7b"
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

# client = MistralClient(api_key=mixtral_api_key)



model = genai.GenerativeModel('gemini-1.5-flash')

chat = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "You are an AI assistant that specializes in extracting the core problem from competitive programming problem statements. Your goal is to identify and present only the essential problem that needs to be solved, removing all extra information.\n\nWhen given a problem statement, follow these steps:\n\n1. Read the problem statement carefully to understand the underlying task.\n2. Identify the core problem that needs to be solved, ignoring all unnecessary details.\n3. Remove the following from the problem statement:\n    - Any background stories, characters, or flavor text\n    - Explanations of the problem or its motivation\n    - Examples demonstrating the problem or its solution\n    - Specific input/output formats or constraints\n    - Scoring information or test case details\n    - Any LaTeX or other formatting syntax\n\n4. Rephrase the core problem concisely in your own words, using as few words as possible while still preserving clarity.\n5. Avoid using any jargon, symbols, extra explanations, or formulas.\n6. Present the core problem directly, without any additional context or commentary.\n7. Review your extracted core problem to ensure it is a complete, standalone statement of the task to be solved, adhering to the steps above.\n\nYour output should be a single, concise statement of the core problem, without any extra information or explanation. The goal is to provide a clear, unambiguous problem statement that captures the essence of the problem, and nothing more.",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Okay, I'm ready to extract the core problems from your competitive programming problem statements. Just provide me with the full problem statement, and I'll analyze it and give you the most concise version of the problem to solve. \n",
      ],
    },
  ]
)

def perform_summarization(text):
    response = chat.send_message(text)
    # messages = [
    #     ChatMessage(role="system", content=summarization_system_prompt),
    #     ChatMessage(role="user", content=text),
    # ]

    # chat_response = client.chat(
    #     model=mixtral_model,
    #     messages=messages
    # )

    # return chat_response.choices[0].message.content
    return response.text


with gr.Blocks() as demo:
    problem = gr.Textbox(label="Problem Statement")
    output = gr.Textbox(label="Summary")
    greet_btn = gr.Button("Summarize")
    greet_btn.click(fn=perform_summarization, inputs=problem, outputs=output, api_name="perform_summarization")



demo.launch(share=True)
