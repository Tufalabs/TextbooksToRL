from .models import QuestionDifficulty

class QuestionPromptTemplates:
    """Class containing templates for question generation prompts."""
    
    @staticmethod
    def question_generation(
        text_book_snippet: str, 
        num_questions: int,
        difficulty: QuestionDifficulty = QuestionDifficulty.UNDERGRAD
    ) -> str:
        return f"""
        You are going to be given a text book snippet.
        Your job is to generate {num_questions} DIFFERENT questions and solutions at {difficulty.value} level.
        
        Difficulty Level: {difficulty.value}
        Level Description: {difficulty.get_description()}
        
        Don't make up new numerical questions, use the ones in the text book snippet.
        Adjust the complexity and depth of analysis based on the specified difficulty level.
        
        Here is the text book snippet:
        {text_book_snippet}

        You MUST generate exactly {num_questions} UNIQUE and DIFFERENT questions and solutions.
        Each question should focus on a different aspect or concept from the text.
        
        Format your response EXACTLY as follows, repeating for EACH of the {num_questions} questions:

        <source>
        [Paste only the relevant part of the source text that relates to this specific question]
        </source>
        <question>
        [Write your unique question here at {difficulty.value} level]
        </question>
        <solution>
        [Write your detailed solution here matching {difficulty.value} level expectations]
        </solution>

        You Should:
        -Focus on generating analytical quantitative questions where possible
        -include all information needed to solve the question from the source text. E.g constants, context etc
        -If final numerical verifiable answer teturn in boxed
        -Match the complexity to {difficulty.value} level
        -Include appropriate mathematical rigor for the level
        -Keep solutions brief and to the point
        
        
        """

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