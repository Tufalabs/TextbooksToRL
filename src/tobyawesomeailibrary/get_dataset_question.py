import random
from datasets import load_dataset
from functools import lru_cache
import json

@lru_cache(maxsize=1)
def load_cached_dataset():
    return load_dataset("lighteval/MATH", split="train")

@lru_cache(maxsize=1)
def load_cached_competition_dataset():
    return load_dataset("hendrycks/competition_math", split="train", trust_remote_code=True)

@lru_cache(maxsize=1)
def load_cached_test_dataset():
    return load_dataset("lighteval/MATH", split="test")

@lru_cache(maxsize=1)
def load_cached_numina_dataset():
    return load_dataset("AI-MO/NuminaMath-CoT", split="train")

@lru_cache(maxsize=1)
def load_cached_skunkworks_dataset():
    return load_dataset("SkunkworksAI/reasoning-0.01", split="train")

@lru_cache(maxsize=1)
def load_cached_mathinstruct_dataset():
    return load_dataset("TIGER-Lab/MathInstruct", split="train")

@lru_cache(maxsize=1)
def load_cached_aslawliet_dataset():
    return load_dataset("aslawliet/olympiads", split="train")

def get_random_math_question():
    # Load the MATH dataset from LightEval (cached)
    dataset = load_cached_dataset()
    

    
    # Get a random index
    random_index = random.randint(0, len(dataset) - 1)
    
    # Get the random question
    random_question = dataset[random_index]
    
    # Extract the problem and solution from the question
    problem = random_question['problem']
    solution = random_question['solution']
    
    return problem, solution

def get_hard_math_question():
    # Load the MATH dataset from LightEval (cached)
    dataset = load_cached_dataset()
    
    # Filter the dataset for Level 5 questions
    hard_questions = [q for q in dataset if q["level"] == "Level 5"]
    
    if not hard_questions:
        raise ValueError("No Level 5 questions found in the dataset")
    
    # Get a random hard question
    random_question = random.choice(hard_questions)
    
    # Extract the problem and solution from the question
    problem = random_question['problem']
    solution = random_question['solution']
    
    return problem, solution


def get_medium_math_question():
    # Load the MATH dataset from LightEval (cached)
    dataset = load_cached_dataset()
    
    # Filter the dataset for Level 5 questions
    hard_questions = [q for q in dataset if q["level"] in ["Level 3", "Level 4", "Level 5"]]
    
    if not hard_questions:
        raise ValueError("No Level 5 questions found in the dataset")
    
    # Get a random hard question
    random_question = random.choice(hard_questions)
    
    # Extract the problem and solution from the question
    problem = random_question['problem']
    solution = random_question['solution']
    
    return problem, solution

def get_competition_math_problem():
    # Load the competition math dataset (cached)
    dataset = load_cached_competition_dataset()
    
    # Get a random index
    random_index = random.randint(0, len(dataset) - 1)
    
    # Get the random question
    random_question = dataset[random_index]
    
    # Extract the problem and solution from the question
    problem = random_question['problem']
    solution = random_question['solution']
    
    return problem, solution

def get_hard_competition_math_problem():
    # Load the competition math dataset (cached)
    dataset = load_cached_competition_dataset()
    
    # Filter the dataset for Level 5 questions
    hard_questions = [q for q in dataset if q["level"] == "Level 5"]
    
    if not hard_questions:
        raise ValueError("No Level 5 questions found in the dataset")
    
    # Get a random hard question
    random_question = random.choice(hard_questions)
    
    # Extract the problem and solution from the question
    problem = random_question['problem']
    solution = random_question['solution']
    
    return problem, solution

def get_gpqa_question():
    # Load the GPQA questions from JSON file
    with open('lib/unique_gpqa_questions.json', 'r') as f:
        questions = json.load(f)
    
    # Get a random question
    random_question = random.choice(questions)
    
    # Extract the problem and solution from the question
    problem = random_question['question']
    solution = random_question['correct_answer']
    explanation = random_question['explanation']
    returned_solution = f"{solution}\n\n{explanation}"
    return problem, returned_solution

def get_test_math_question():
    # Load the MATH test dataset (cached)
    dataset = load_cached_test_dataset()
    
    # Get a random index
    random_index = random.randint(0, len(dataset) - 1)
    
    # Get the random question
    random_question = dataset[random_index]
    
    # Extract the problem and solution from the question
    problem = random_question['problem']
    solution = random_question['solution']
    
    return problem, solution

def get_test_gpqa_question():
    # Load the GPQA test questions from JSON file
    with open('lib/unique_gpqa_test_questions.json', 'r') as f:
        questions = json.load(f)
    
    # Get a random question
    random_question = random.choice(questions)
    
    # Extract the problem and solution from the question
    problem = random_question['question']
    solution = random_question['correct_answer']
    explanation = random_question['explanation']
    returned_solution = f"{solution}\n\n{explanation}"
    return problem, returned_solution

def get_custom_question():
    # Load the custom questions from JSON file
    try:
        with open('lib/custom_questions.json', 'r') as f:
            data = json.load(f)
            questions = data['questions']
            problem = random.choice(questions)
            solution = "No solution provided. Please verify your answer independently."
        
        return problem, solution
    except FileNotFoundError:
        raise FileNotFoundError("custom_questions.json not found in lib directory")
    except KeyError:
        raise KeyError("custom_questions.json must contain a 'questions' array")
    except json.JSONDecodeError:
        raise ValueError("custom_questions.json is not valid JSON")

def get_numina_math_question():
    # Load the NuminaMath dataset (cached)
    dataset = load_cached_numina_dataset()
    
    # Get a random index
    random_index = random.randint(0, len(dataset) - 1)
    
    # Get the random question
    random_question = dataset[random_index]
    
    # Extract the problem and solution from the question
    problem = random_question['problem']
    solution = random_question['solution']
    
    return problem, solution

def get_skunkworks_question():
    # Load the Skunkworks dataset (cached)
    dataset = load_cached_skunkworks_dataset()
    
    # Get a random index
    random_index = random.randint(0, len(dataset) - 1)
    
    # Get the random question
    random_question = dataset[random_index]
    
    # Extract the problem and solution from the question
    problem = random_question['instruction']
    solution = random_question['reasoning']
    
    return problem, solution

def get_mathinstruct_question():
    # Load the MathInstruct dataset (cached)
    dataset = load_cached_mathinstruct_dataset()
    
    # Get a random index
    random_index = random.randint(0, len(dataset) - 1)
    
    # Get the random question
    random_question = dataset[random_index]
    
    # Extract the problem and solution from the question
    problem = random_question['instruction']
    solution = random_question['output']
    
    return problem, solution

@lru_cache(maxsize=1)
def get_cached_olympiad_questions():
    dataset = load_cached_numina_dataset()
    return [q for q in dataset if q["source"] == "olympiads"]

def get_numina_olympiad_question(count=1):
    # Use cached filtered questions
    olympiad_questions = get_cached_olympiad_questions()
    
    if not olympiad_questions:
        raise ValueError("No olympiad questions found in the dataset")
    
    # Get random olympiad questions
    if count == 1:
        random_question = random.choice(olympiad_questions)
        return random_question['problem'], random_question['solution']
    else:
        sample_size = min(count, len(olympiad_questions))
        random_questions = random.sample(olympiad_questions, sample_size)
        return [(q['problem'], q['solution']) for q in random_questions]

def get_aslawliet_olympiad_question():
    # Load the aslawliet/olympiads dataset (cached)
    dataset = load_cached_aslawliet_dataset()
    
    # Get a random index
    random_index = random.randint(0, len(dataset) - 1)
    
    # Get the random question
    random_question = dataset[random_index]
    
    # Extract the problem and solution from the question
    # Note: Column names are 'problem' and 'has solution'
    problem = random_question['problem']
    solution = random_question['solution']
    
    return problem, solution

# Example usage
if __name__ == "__main__":
    random_problem, random_solution = get_random_math_question()
    print("Random MATH question:")
    print("Problem:", random_problem)
    print("\nSolution:", random_solution)

    print("\nHard MATH question:")
    hard_problem, hard_solution = get_hard_math_question()
    print("Problem:", hard_problem)
    print("\nSolution:", hard_solution)

    print("\nCompetition MATH question:")
    comp_problem, comp_solution = get_competition_math_problem()
    print("Problem:", comp_problem)
    print("\nSolution:", comp_solution)

    print("\nHard Competition MATH question:")
    hard_comp_problem, hard_comp_solution = get_hard_competition_math_problem()
    print("Problem:", hard_comp_problem)
    print("\nSolution:", hard_comp_solution)

    print("\nTest set MATH question:")
    test_problem, test_solution = get_test_math_question()
    print("Problem:", test_problem)
    print("\nSolution:", test_solution)

    print("\nGPQA test question:")
    gpqa_test_problem, gpqa_test_solution = get_test_gpqa_question()
    print("Problem:", gpqa_test_problem)
    print("\nSolution:", gpqa_test_solution)

    print("\nCustom question:")
    custom_problem, custom_solution = get_custom_question()
    print("Problem:", custom_problem)
    print("\nSolution:", custom_solution)

    print("\nNuminaMath question:")
    numina_problem, numina_solution = get_numina_math_question()
    print("Problem:", numina_problem)
    print("\nSolution:", numina_solution)

    print("\nSkunkworks reasoning question:")
    skunk_problem, skunk_solution = get_skunkworks_question()
    print("Problem:", skunk_problem)
    print("\nSolution:", skunk_solution)

    print("\nMathInstruct question:")
    math_inst_problem, math_inst_solution = get_mathinstruct_question()
    print("Problem:", math_inst_problem)
    print("\nSolution:", math_inst_solution)

    print("\nNumina Math Olympiad question:")
    olympiad_problem, olympiad_solution = get_numina_olympiad_question()
    print("Problem:", olympiad_problem)
    print("\nSolution:", olympiad_solution)

    print("\nAslawliet Olympiad question:")
    aslawliet_problem, aslawliet_solution = get_aslawliet_olympiad_question()
    print("Problem:", aslawliet_problem)
    print("\nSolution:", aslawliet_solution)
