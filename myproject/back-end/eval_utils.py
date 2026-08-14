import json
import datasets
import torch

from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

def load_beavertails():
    """ return a single dataset of beavertails"""
    ds = load_dataset("PKU-Alignment/BeaverTails")
    print(list(ds.keys()))
    ds = ds["30k_test"]
    return ds 

def load_model(model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map={"": "cpu"},
        quantization_config=BitsAndBytesConfig(load_in_4bit=True),
    )
    return tokenizer, model


def dump_prompts(ds, path="prompts.json"):
    """dedupe prompts into a {prompt: true} json blob (poor man's hashset)"""
    prompts = {row["prompt"]: True for row in ds}
    with open(path, "w") as f:
        json.dump(prompts, f, indent=2)
    print(f"dumped {len(prompts)} unique prompts to {path}")
    return prompts


def make_response(model,tokenizer,prompt):
    messages = [
        {"role": "user", "content":  prompt},
    ]
    inputs = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
    ).to(model.device)

    outputs = model.generate(**inputs, max_new_tokens=300)
    return tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1]:])


def generate_responses(model, tokenizer, prompts, path="responses.json"):
    """generate a response for each prompt, dump {prompt: response} to json"""
    results = {}
    for i, prompt in enumerate(prompts):
        print(f"[{i+1}/{len(prompts)}] {prompt[:60]}...")
        results[prompt] = make_response(model, tokenizer, prompt)
        with open(path, "w") as f:
            json.dump(results, f, indent=2)
    print(f"dumped {len(results)} responses to {path}")
    return results


def main():
    ds = load_beavertails()
    print(ds)
    print(ds[0])
    prompts = dump_prompts(ds)
    tokenizer, model = load_model("Qwen/Qwen3-4B")
    generate_responses(model, tokenizer, prompts)
if __name__ == "__main__":
    main()