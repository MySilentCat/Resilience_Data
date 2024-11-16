from transformers import AutoModel, AutoTokenizer

def run_codet5p_bimodal(code):
    checkpoint = "Salesforce/codet5p-220m-bimodal"
    device = "cpu"  # for GPU usage or "cpu" for CPU usage

    tokenizer = AutoTokenizer.from_pretrained(checkpoint, trust_remote_code=True)
    model = AutoModel.from_pretrained(checkpoint, trust_remote_code=True).to(device)

    input_ids = tokenizer(code, return_tensors="pt").input_ids.to(device)

    generated_ids = model.generate(input_ids, max_length=20)
    print(tokenizer.decode(generated_ids[0], skip_special_tokens=True))
    # Convert a string of SVG data to an image.

if __name__ == "__main__":
    code_file = r"E:\Graduation_Design\Input_process\test\saolei\code\main.c"
    run_codet5p_bimodal(code_file)