# IPC: Intelligent Programming Companion

## Introduction

The field of Computer Science (CS) is characterized by its rapid evolution and the constant need for learning among students, employees, and employers. Problem-solving, a crucial and popular domain within CS, demands continuous practice and skill enhancement. A key question in this field is: "How can one best prepare for interviews and competitive programming contests?"

Despite the existence of numerous platforms hosting diverse problems, several significant issues impact both interview preparation and competitive programming:

1. **Repetition and Uniqueness**: Problem setters often unknowingly create similar problems, leading to repetition. This gives an unfair advantage to those familiar with these problems and reduces the overall value of problem sets.

2. **Difficulty Assessment**: Problem setters frequently struggle to determine the appropriate difficulty level for their problems, resulting in inconsistent assessments that hinder effective preparation and fair competition.

3. **Platform Fragmentation**: The absence of a centralized platform for problem setters to share and collaborate results in problems being scattered across multiple websites, causing confusion and making it difficult for individuals to find suitable practice problems.

4. **Clarity of Problem Descriptions**: Many problem descriptions lack clarity, posing challenges for both human solvers and AI tools. Unclear problem statements hinder accurate comprehension and effective problem-solving.

IPC (Intelligent Programming Companion) aims to address these challenges comprehensively. By grouping problems, reducing repetition, refining problem descriptions, and providing intelligent tools for problem-solving and preparation, IPC seeks to create a more cohesive and supportive environment for competitive programmers and software engineer interview candidates.

## IPC: A Comprehensive Solution

IPC is a centralized platform designed to enhance the competitive programming and interview preparation experience. It leverages cutting-edge AI techniques to:

- **Summarize Problem Statements:** Generate concise summaries of complex problems, improving comprehension and reducing time spent on reading.
- **Identify Similar Problems and Solutions:** Help users discover related problems and solutions, fostering knowledge sharing and preventing unnecessary repetition.
- **Predict Problem Difficulty and Assign Relevant Tags:** Enable users to easily find problems matching their skill level and interests.
- **Provide Dynamic Problem-Solving Assistance:** Offer an interactive chatbot to assist with code generation and understanding, promoting independent learning.

## Key Features

- **Problem Summarization**: Utilizes Google's Gemini 1.5 architecture with advanced prompt engineering to generate concise summaries of complex problem statements.
- **Similarity Module**: Implements nearest-vector approach with state-of-the-art vector databases to find similar problems and solutions with high accuracy.
- **Difficulty/Tags Prediction**: Applies BigBird BERT-based architecture for accurate predictions of problem difficulty levels and relevant tags.
- **Solver Module**: Interactive chatbot built on RAG architecture with CodeQwen LLM for robust code generation and understanding.

## Performance Highlights

- **Similarity Module:** Achieves a remarkable **97.5% recall@10** on problem statements and **99.6% recall@10** on solutions, demonstrating the effectiveness of the nearest-vector approach.
- **Difficulty/Tags Prediction:** Exhibits robust performance with an ROC AUC score of **76.37%**, accurately predicting problem difficulty levels and assigning relevant tags.

## Dataset

The project uses a comprehensive dataset of programming problems and solutions collected from various online judges:

| Online Judge | Number Of Problems | Number Of Solutions |
| ------------ | ------------------ | ------------------- |
| AtCoder      | 2307               | 1,587,756           |
| CodeChef     | 3201               | 53,961              |
| CSES         | 296                | 1,175               |
| Codeforces   | 8636               | 16,229              |
| HackerEarth  | 985                | 36,179              |
| LeetCode     | 2424               | 3,570               |
| Uva          | 1461               | 1,347               |
| Yosupo       | 193                | 195                 |

To ensure the modules focus on the functional aspects of the source code and problem statements, we applied comprehensive preprocessing steps to both solutions and problems. dataset.

**For Solutions:**

- Removal of `#include` directives, `using namespace` statements, and comments.
- Removal of non-ASCII characters.
- Identification and removal of unused functions using the `cpp-check` tool.
- Tokenization of source code using the `pygments` library.

**For Problems:**

- Substitution of exponential notation with numeric equivalents.
- Insertion of spaces between dollar signs.
- Conversion of text to lowercase.
- Simplification of mathematical expressions.
- Removal of common stopwords using the `nltk` library.
- Lemmatization of words using the `nltk` library.

These preprocessing steps ensured that the data fed into our models was clean, consistent, and focused on the functional and relevant aspects of the problems and solutions, enhancing the performance and accuracy of our modules.

## Conclusion

Our proposed solution, IPC (Intelligent Programming Companion), addresses significant challenges in competitive programming and interview preparation. By integrating modules focused on problem uniqueness, solver efficiency, difficulty prediction, and problem clarity, IPC aims to create a more cohesive and supportive environment for programmers.

The implemented modules – Summarization, Similarity, Difficulty/Tags Prediction, and Solver – have demonstrated strong performance metrics. Notably, the Similarity Module achieved a remarkable 99.6% recall@10, indicating its efficacy in identifying similar problems and ensuring problem set originality. The Difficulty/Tags Prediction Module showed robust performance with a ROC AUC score of 76.37%, effectively guiding users in problem selection based on difficulty levels and relevant tags.

These findings underscore the significance of integrated platforms in overcoming existing challenges and improving learning outcomes. By addressing issues such as problem repetition, inconsistent difficulty assessments, platform fragmentation, and ambiguous problem descriptions, IPC aims to:

- Streamline problem-solving processes.
- Foster innovation and knowledge sharing within the community.
- Create a more supportive environment for competitive programmers and interview candidates.

Our research lays the groundwork for future advancements in Computer Science education and problem-solving methodologies.

## Contributors & Contact Information

- Yosef Madboly (20201701037@cis.asu.edu.eg)
- Salma Mahdy (20201700353@cis.asu.edu.eg)
- Mohamed Hesham (20201701245@cis.asu.edu.eg)
- Salma Ayman (20201700345@cis.asu.edu.eg)
- Omar Yasser (20201701195@cis.asu.edu.eg)
- Martina Angelos (20201700624@cis.asu.edu.eg)

> **For more Information, please contact us via email or check the Documentation [here](./IPC%20Documentation.docx) for more details.**
