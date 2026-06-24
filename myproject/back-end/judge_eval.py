import transformers
import torch
import os
import json
import datasets
from huggingface_hub import login
from dotenv import load_dotenv



NINEBILLION = "Qwen/Qwen3.5-9B"
FOURBILLION = "Qwen/Qwen3.5-4B"

BEAVERTAILS = "PKU-Alignment/BeaverTails"

load_dotenv()


def load_beavertails(split="30k_test"):
    """Load a BeaverTails split. Each row has: prompt, response,
    category (14 harm flags), is_safe (bool ground-truth label)."""
    ds = datasets.load_dataset(BEAVERTAILS, split=split)
    print(f"BeaverTails[{split}]: {len(ds):,} rows")
    n_safe = sum(ds["is_safe"])
    print(f"  safe: {n_safe:,} ({n_safe / len(ds):.1%})  unsafe: {len(ds) - n_safe:,}")
    return ds


def main():
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    login(token=os.getenv("HUGGINGFACEHUB_API_TOKEN"))
    dataset = load_beavertails()
    if torch.cuda.is_available():
        device = "cuda"
        print(f"CUDA available: {torch.cuda.get_device_name(0)}")
        print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    else:
        device = "cpu"
        print("CUDA not available, running on CPU (will be slow for a 9B model)")
    if device == "cuda":
        # 8-bit quantization so the 4B model fits in 8 GB VRAM (~4.5 GB)
        quant_config = transformers.BitsAndBytesConfig(load_in_8bit=True)
        model = transformers.AutoModelForCausalLM.from_pretrained(
            FOURBILLION,
            quantization_config=quant_config,
            device_map="auto",
        )
    else:
        model = transformers.AutoModelForCausalLM.from_pretrained(FOURBILLION)
    tokenizer = transformers.AutoTokenizer.from_pretrained(FOURBILLION)

    results = []
    for i in range(10):
        prompt = dataset[i]["prompt"]
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        outputs = model.generate(**inputs, max_new_tokens=256)
        # decode only the generated continuation, not the echoed prompt
        response = tokenizer.decode(
            outputs[0][inputs["input_ids"].shape[-1]:], skip_special_tokens=True
        )
        results.append({"Pair": {"prompt": prompt, "response": response}})
        print(f"[{i + 1}/100] {prompt[:60]}")

    with open("responses.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(results)} responses to responses.json")




if __name__ == "__main__":
    main()