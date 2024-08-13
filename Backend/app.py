from flask import Flask, request, jsonify
from kaggle import kaggleAPI
import pandas as pd 
from problems_similarity import DocumentSearch
from solutions_similarity import CodeSearch
import difficulty
import json 

app = Flask(__name__)

def load_problems_similarity():
    global problems_search_engine
    csv_file_path = 'problems_similarity_dump/combined_problems_with_summarization.csv'
    df = pd.read_csv(csv_file_path)
    problems_search_engine = DocumentSearch(df)
    problems_search_engine.load_model()
    problems_search_engine.load_faiss_index()

def load_solutions_similarity():
    global solutions_search_engine
    csv_file_path = 'solutions_similarity_dump/preprocessed_solutions_v1.csv'
    df = pd.read_csv(csv_file_path)
    solutions_search_engine = CodeSearch(df)
    solutions_search_engine.load_faiss_index()

def load_difficulty():
    global difficulty_kaggle_api
    notebook_id = 'omar0yasser/difficulty-prediction-prod'
    difficulty_kaggle_api = kaggleAPI(notebook_id, 'difficulty')
    difficulty_kaggle_api.pull_kaggle_notebook()
    
def init():
    load_problems_similarity()
    load_solutions_similarity()
    load_difficulty()

@app.route('/difficulty', methods=['POST'])
def estimate_difficulty():
    problem = request.json['problem']
    return perform_difficulty_estimation(problem)

@app.route('/similarity_problem', methods=['POST'])
def similarity_problem():
    problem = request.json['problem']
    top_k = request.json['top_k']
    # problem = perform_summarization(problem)
    similar_problems = problems_search_engine.query(problem, top_k)
    return similar_problems

@app.route('/similarity_solution', methods=['POST'])
def similarity_solution():
    solution = request.json['solution']
    top_k = request.json['top_k']
    similar_solutions = solutions_search_engine.query(solution, top_k)
    return similar_solutions

def perform_difficulty_estimation(text):
    difficulty.update_inference_parameter('difficulty/notebook/difficulty-prediction-prod.ipynb', text)
    difficulty_kaggle_api.push_kaggle_notebook()
    difficulty_kaggle_api.wait_for_notebook_completion()
    difficulty_kaggle_api.get_notebook_output()

    json_path = 'difficulty/nb_output/result.json'
    with open(json_path, 'r') as f:
        data = json.load(f)    
    return jsonify(data)

if __name__ == '__main__':
    init()
    app.run(host='0.0.0.0', port=5555, debug=False)
