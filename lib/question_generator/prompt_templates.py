from .models import QuestionDifficulty

class QuestionPromptTemplates:
    """Class containing templates for question generation prompts."""
    
    @staticmethod
    def question_generation(
        text_book_snippet: str, 
        num_questions: int,
        difficulty: QuestionDifficulty = QuestionDifficulty.GRAD
    ) -> str:
        return f"""
  I'm trying to quiz myself on this text to help me learn

  
  can you generate between {num_questions} and {num_questions * 3} questions and solutions for me?

  Can you focus on problems that have numerical answers and can you output the answer in a box?

  Leave final answer as fraction no need to express as decimal.

  Make sure each problem has the full context of the problem in the question.

   For each problem, follow the exact format below:


   <question>
   [Write your unique math problem here at {difficulty.value} level. Ensure that the problem statement includes all necessary details and context from the snippet so it is fully self-contained.]
   </question>
   <solution>
   [Write your detailed solution here matching {difficulty.value} level expectations. Ensure that if a final numerical answer is provided, it is enclosed in a box.]
   </solution>


Textbook Snippet:
{text_book_snippet}
        
"""
#         return f"""
#         You are given a textbook snippet. Your task is to generate questions and solutions based solely on the provided snippet. Follow these instructions precisely:

# 1. **Source Dependency:**  
#    - Only use information directly from the snippet. Do not infer or include any external information.
#    - Every question must be verifiable and solvable using only the information contained in the snippet.

# 2. **Question and Quantity Requirements:**  
#    - Generate between {num_questions} and {num_questions * 3} UNIQUE and DIFFERENT questions.
#    - If the snippet does not support {num_questions} distinct questions, generate only as many as can be fully supported by the text.

# 3. **Difficulty Level Specification:**  
#    - Match the complexity and depth of analysis to {difficulty.value} level.
#    - Include appropriate mathematical rigor and analytical reasoning expected at this level.

# 4. **Question Self-Containment:**  
#    - Ensure each question is fully self-contained. Include all numerical values, constants, and context from the snippet necessary to solve the question.
#    - If the question involves a derivation or an expression, show the initial expression and the steps leading to the final answer.

# 5. **Answer Presentation:**  
#    - If the solution yields a final numerical answer, enclose that result in a box (using LaTeX or a similar method).
#    - Keep solutions brief and to the point while ensuring all necessary details are included.

# 6. **Response Format:**  
#    For each question, repeat the following format EXACTLY:

#    <source>
#    [Paste only the relevant part of the textbook snippet that directly supports and contains the solution for this question]
#    </source>
#    <question>
#    [Write your unique question here at {difficulty.value} level]
#    </question>
#    <solution>
#    [Write your detailed solution here matching {difficulty.value} level expectations]
#    </solution>

# 7. **No Extraneous Information:**  
#    - Do not include any commentary, introductions, or additional text outside the prescribed format.
#    - Every piece of output must strictly adhere to the structure above.

# Textbook Snippet:
# {text_book_snippet}

# Begin generating the questions and solutions now.

#         """

    @staticmethod
    def hint_generation(
        question: str,
        difficulty: QuestionDifficulty = QuestionDifficulty.UNDERGRAD
    ) -> str:
        return f"""
        You are a helpful teaching assistant working with {difficulty.value} level students.
        A student is struggling with this {difficulty.value} level question.
        Generate 2-3 helpful hints that will guide them toward the solution without giving it away.
        
        The hints should:
        1. Break down the problem-solving approach into steps appropriate for {difficulty.value} level
        2. Point out key concepts or equations to consider
        3. Suggest what to focus on first
        4. Match the theoretical depth expected at {difficulty.value} level
        
        Question:
        {question}

        Format your response as:
        <hints>
        1. [First hint appropriate for {difficulty.value} level]
        2. [Second hint with {difficulty.value} appropriate complexity]
        3. [Optional third hint if needed]
        </hints>
        """ 