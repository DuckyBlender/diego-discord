import mlx_lm
from mlx_lm.sample_utils import make_sampler
from mlx_lm.models.cache import make_prompt_cache

def load_model():
    model, tokenizer = mlx_lm.load("DuckyBlender/diegogpt-v2-mlx-bf16")
    cache = make_prompt_cache(model)
    return model, tokenizer, cache

def generate_response(model, tokenizer, user_input, cache):
    if tokenizer.chat_template is not None:
        messages = [
            {"role": "system", "content": "/no_think"},
            {"role": "user", "content": user_input}
        ]
        prompt = tokenizer.apply_chat_template(messages, add_generation_prompt=True, tokenize=False, enable_thinking=False)
    else:
        prompt = user_input

    sampler = make_sampler(temp=0.7, top_p=0.8, top_k=20, min_p=0)

    response = mlx_lm.generate(
        model,
        tokenizer,
        prompt=prompt,
        sampler=sampler,
        prompt_cache=cache,
        verbose=True
    )
    
    return response