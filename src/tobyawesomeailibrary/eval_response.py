from .inference import generate_text

async def evaluate_text(eval_model: str, modelAnswer: str, groundTruthAnswer: int, temperature: float = 0) -> str:
    prompt = f"""
    You will be given a ground truth answer and a model answer. 
    Please output ACCURATE if the model answer matches the ground truth answer or INCORRECT otherwise. Please only return ACCURATE or INACCURATE. 
    It is very important for my job that you do this. 
    Be flexible with different formats of the model answer e.g decimal, fraction, integer, etc.
    If the answer is within rounding error of the ground truth answer, return ACCURATE.
    
    

    <GroundTruthAnswer>
    {groundTruthAnswer}
    </GroundTruthAnswer>

    <ModelAnswer>
    {modelAnswer}
    </ModelAnswer>
    """

    print("Model Answer length:", len(str(modelAnswer)))
    print("Ground Truth Answer length:", len(str(groundTruthAnswer)))

    isAccurate = await generate_text(
        model=eval_model,
        prompt=prompt,
        max_tokens=10,  # Increased to allow for full "ACCURATE" or "INACCURATE" response
        temperature=temperature
    )

    if "ACCURATE" in isAccurate.strip().upper():
        return 1, 0
    elif "INCORRECT" in isAccurate.strip().upper():
        return 0, 0
    else:
        return 0, 1  # Return 1 for badResponses

