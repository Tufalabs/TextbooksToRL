from question_generator import QuestionGenerator

async def main():
    # Example passage
    passage = """
    In calculus, a sequence is a list of numbers in a definite order. 
    The limit of a sequence {an} is the value that the terms of the sequence approach as n approaches infinity.
    For example, the sequence an = 1/n approaches 0 as n approaches infinity.
    """
    
    # Create question generator
    generator = QuestionGenerator()
    
    # Generate questions with verification
    print("Generating questions with verification...")
    verified_questions = await generator.generate_questions(
        passage,
        num_questions=3,
        verify=True,
        verification_threshold=0.8
    )
    
    print(f"\nGenerated {len(verified_questions)} verified questions:")
    for i, qa in enumerate(verified_questions, 1):
        print(f"\nQuestion {i}:")
        print(qa.question)
        print("\nSolution:")
        print(qa.solution)
        print("\nHints:")
        for j, hint in enumerate(qa.hints or [], 1):
            print(f"{j}. {hint}")
        print("-" * 80)
    
    # Generate questions without verification
    print("\nGenerating questions without verification...")
    unverified_questions = await generator.generate_questions(
        passage,
        num_questions=3,
        verify=False
    )
    
    # Example of validating a student solution
    student_solution = """
    The limit of 1/n as n approaches infinity is 0 because as n gets larger,
    1/n becomes increasingly smaller, approaching but never reaching 0.
    """
    
    validation_result = await generator.validate_solution(
        verified_questions[0].question,
        student_solution,
        verified_questions[0].solution
    )
    
    print(f"\nStudent solution is {'correct' if validation_result.is_correct else 'incorrect'}")
    print(f"Score: {validation_result.score}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 