class QuestionPromptTemplates:
    """Class containing templates for question generation prompts."""
    
    @staticmethod
    def question_generation(text_book_snippet: str, num_questions: int) -> str:
        return f"""
        You are going to be given a text book snippet.
        Your job is to generate {num_questions} DIFFERENT questions and solutions.
        Don't make up new numerical questions, use the ones in the text book snippet.
        
        Here is the text book snippet:
        {text_book_snippet}

        You MUST generate exactly {num_questions} UNIQUE and DIFFERENT questions and solutions.
        Each question should focus on a different aspect or concept from the text.
        
        Format your response EXACTLY as follows, repeating for EACH of the {num_questions} questions:

        <source>
        [Paste only the relevant part of the source text that relates to this specific question]
        </source>
        <question>
        [Write your unique question here]
        </question>
        <solution>
        [Write your detailed solution here]
        </solution>

        Make sure to:
        1. Generate EXACTLY {num_questions} DIFFERENT questions
        2. Make each question unique and distinct from the others
        3. Include ALL XML tags for EACH question
        4. Use proper XML formatting with no nested tags
        5. Base questions on different aspects of the source text
        6. Include only the relevant portion of the source text for each question
        
        DO NOT:
        1. Repeat the same question with different wording
        2. Use the entire source text for each question
        3. Focus on the same concept for multiple questions
        """

    @staticmethod
    def hint_generation(question: str) -> str:
        return f"""
        You are a helpful teaching assistant. A student is struggling with this question.
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