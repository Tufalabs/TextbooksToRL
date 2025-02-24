class QuestionPromptTemplates:
    """Class containing templates for question generation prompts."""
    
    @staticmethod
    def question_generation(text_book_snippet: str, num_questions: int) -> str:
        return f"""
        You are going to be given a text book snippet.
        Your job is to generate sample questions and solutions to these questions.
        Don't make up new numerical questions, use the ones in the text book snippet.
        Here is the text book snippet:
        {text_book_snippet}

        Also include the SOURCE TEXT in the response which is the text book snippet that you are using to generate the questions and solutions.

        You should follow the following format:
        <source>SOURCE TEXT</source>
        <question>QUESTION TEXT</question>
        <solution>SOLUTION TEXT</solution>
        
        You should generate {num_questions} questions and solutions.

        You questions should be hard, use examples from the text book snippet and sample calculations.

        Things like derive this relation, solve this problem and theory questions are best.
        """

    @staticmethod
    def hint_generation(question: str) -> str:
        return f"""
        You are a helpful teaching assistant. A student is struggling with this physics question.
        Generate 2-3 helpful hints that will guide them toward the solution without giving it away.
        The hints should:
        1. Break down the problem-solving approach into steps
        2. Point out key concepts or equations to consider
        3. Suggest what to focus on first
        
        Question:
        {question}

        Format your response as:
        <hints>
        1. [First hint]
        2. [Second hint]
        3. [Optional third hint if needed]
        </hints>
        """ 