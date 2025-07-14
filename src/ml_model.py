from langchain_community.llms import MLXPipeline
from transformers import AutoTokenizer

def load_model(model_id="DuckyBlender/diegogpt-v2-mlx-bf16"):  # Replace with your actual MLX-compatible Qwen model ID
    # Load the MLX pipeline with the Qwen model
    llm = MLXPipeline.from_model_id(model_id)
    
    # Load the corresponding tokenizer from Hugging Face
    tokenizer = AutoTokenizer.from_pretrained(model_id, add_generation_prompt=True, use_fast=True)  # Use fast tokenizer for better performance
    return llm, tokenizer

def generate_response(llm, tokenizer, messages):
    formatted_input = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False
    )
    
    # Generate response with your pipeline kwargs
    response = llm.invoke(
        formatted_input,
        pipeline_kwargs={
            "temp": 0.7, 
            "top_p": 0.8, 
            "min_p": 0.0,
            "top_k": 20,
            "max_tokens": 128, 
            "repetition_penalty": 1.5,
            "repetition_context_size": 20,
            "verbose": True
        }
    )
    
    return response
