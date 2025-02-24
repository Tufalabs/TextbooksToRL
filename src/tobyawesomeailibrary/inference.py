import os
import openai
import anthropic
import aiohttp
import json
from typing import Optional, Dict, Any
from openai import AsyncOpenAI
import asyncio
import requests

# API Keys
openai_api_key = "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"
anthropic_api_key = "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"
deepseek_api_key = "sk-001083745c96497dad47fbbda4114467"
deepinfra_api_key = "1p4JUUNWSJ2sOwxFk7AKbT4eaIJ9VcVq"

# Initialize clients
async_openai_client = AsyncOpenAI(api_key=openai_api_key)

deepseek_client = AsyncOpenAI(
    api_key=deepseek_api_key,
    base_url="https://api.deepseek.com"
)

# Add DeepInfra API key
deepinfra_api_key = "1p4JUUNWSJ2sOwxFk7AKbT4eaIJ9VcVq"

# Add DeepInfra client initialization
deepinfra_client = AsyncOpenAI(
    api_key=deepinfra_api_key,
    base_url="https://api.deepinfra.com/v1/openai"
)

async def generate_text(model: str, prompt: str, max_tokens: int = 8000, temperature: float = 0) -> str:
    """
    Asynchronously generate text using various AI models.
    
    :param model: The name of the model to use (e.g., "gpt-3.5-turbo", "claude-2", "meta-llama/Llama-2-70b-chat-hf")
    :param prompt: The input prompt for text generation
    :param max_tokens: Maximum number of tokens to generate
    :param temperature: Controls randomness in generation (0.0 to 1.0)
    :return: Generated text as a string
    """
    
    # OpenAI models
    if model.startswith("gpt-") or model.startswith("o1"):
        response = await async_openai_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content.strip()
    
    elif model.startswith("ft:gpt") or model.startswith("o1"):
        response = await async_openai_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content.strip()
    
    # Anthropic (Claude) models
    elif model.startswith("claude-"):
        async def run_anthropic():
            client = anthropic.Anthropic(api_key=anthropic_api_key)
            if model.startswith("claude-3"):
                response = client.messages.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                return response.content[0].text.strip()
            else:
                response = client.completions.create(
                    model=model,
                    prompt=f"Human: {prompt}\n\nAssistant:",
                    max_tokens_to_sample=max_tokens,
                    temperature=temperature
                )
                return response.completion.strip()
        
        return await run_anthropic()
    
    # DeepInfra models
    elif model.startswith("meta-llama/") or model.startswith("deepseek-ai") or model.startswith("Qwen/") or model.startswith("Meta-Llama"):
        response = await deepinfra_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content.strip()
    
    # DeepSeek models
    elif model.startswith("deepseek-"):
        response = await deepseek_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content.strip()
    
    else:
        raise ValueError(f"Unsupported model: {model}")
