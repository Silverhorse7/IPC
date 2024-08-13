## IPC: Intelligent Programming Companion

**Introduction:**

The world of competitive programming and software engineering interviews is a challenging one, demanding constant learning and practice. While numerous platforms offer problem sets, several key issues hinder effective preparation and fair competition:

* **Problem Repetition:**  Similar problems across platforms give an unfair advantage to those familiar with them, diminishing the value of practice.
* **Inconsistent Difficulty Assessments:**  Unreliable difficulty ratings make it difficult to choose suitable problems for practice and can lead to unfair comparisons.
* **Platform Fragmentation:**  Scattered problems across multiple websites create confusion and make it difficult to find the right problems for specific learning goals.
* **Ambiguous Problem Descriptions:**  Unclear problem statements can impede comprehension and hinder effective problem-solving.

**IPC: A Comprehensive Solution**

To address these challenges, we introduce IPC (Intelligent Programming Companion), a centralized platform designed to enhance the competitive programming and interview preparation experience. 

IPC leverages cutting-edge AI techniques to:

* **Summarize Problem Statements:** Generate concise summaries of complex problems, improving comprehension and reducing time spent on reading.
* **Identify Similar Problems and Solutions:**  Help users discover related problems and solutions, fostering knowledge sharing and preventing unnecessary repetition.
* **Predict Problem Difficulty and Assign Relevant Tags:**  Enable users to easily find problems matching their skill level and interests.
* **Provide Dynamic Problem-Solving Assistance:**  Offer an interactive chatbot to assist with code generation and understanding, promoting independent learning.

**This Repository:**

This repository contains the code and documentation for IPC, enabling researchers and developers to explore its functionality and contribute to its ongoing development.

**Key Features:**

* **Problem Summarization:**  Utilizes advanced prompt engineering techniques with Gemini 1.5 to generate concise summaries of complex problem statements.
* **Problem/Solution Similarity Detection:** Employs the nearest-vector approach with state-of-the-art vector databases to find similar problems and solutions, achieving high recall rates.
* **Difficulty/Tags Prediction:**  Leverages a BigBird BERT-based architecture to accurately predict problem difficulty levels and assign relevant tags.
* **Solver Module:** Provides an interactive chatbot for dynamic problem-solving, built on a RAG architecture with CodeQwen LLM for robust code generation and understanding.

**Performance and Results:**

**4.1 Dataset**

We collected a comprehensive dataset of problems and their corresponding solutions, scraped from various online judges and GitHub repositories. The dataset comprises 19,503 problems and 1,700,412 solutions.

**Table 4.1: Problems Dataset Details**

| Online Judge    | Number of Problems |
|-----------------|--------------------|
| AtCoder         | 2,307              |
| CodeChef        | 3,201              |
| CSES            | 296               |
| Codeforces      | 8,636              |
| HackerEarth     | 985               |
| LeetCode        | 2,424              |
| UVa             | 1,461              |
| Yosupo         | 193               |

**Table 4.2: Solutions Dataset Details**

| Online Judge    | Number of Solutions |
|-----------------|----------------------|
| AtCoder         | 1,587,756            |
| CodeChef        | 53,961              |
| CSES            | 1,175               |
| Codeforces      | 16,229              |
| HackerEarth     | 36,179              |
| LeetCode        | 3,570               |
| UVa             | 1,347               |
| Yosupo         | 195                |

**Preprocessing:**

To ensure the modules focus on the functional aspects of the source code and problem statements, we applied comprehensive preprocessing steps, including:

* **Solutions:** Removal of #include directives, using namespace, comments, non-ASCII characters, unused functions, and tokenization. 
* **Problems:**  Substitution of exponential notation, insertion of spaces between dollar signs, conversion to lowercase, calculation of expressions, removal of stopwords, and lemmatization.

**Performance Highlights:**

* **Problem/Solution Similarity Detection:** Achieves a remarkable **97.5% recall@10** on problem statements and **99.6% recall@10** on solutions, demonstrating the effectiveness of the nearest-vector approach.
* **Difficulty/Tags Prediction:**  Exhibits robust performance with an ROC AUC score of **76.37%**, accurately predicting problem difficulty levels and assigning relevant tags.

**Join us in building a better programming ecosystem!**