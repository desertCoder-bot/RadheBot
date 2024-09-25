from flask import Flask, render_template, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

app = Flask(__name__)

print("Model loading started...")
models = {
    "gpt2": "gpt2",
    "tinyllama": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    "distilgpt2": "distilgpt2",
    "blenderbot": "facebook/blenderbot-400M-distill",
    "dialogpt": "microsoft/DialoGPT-medium"
}

tokenizers = {}
model_instances = {}

for name, model_path in models.items():
    try:
        tokenizers[name] = AutoTokenizer.from_pretrained(model_path)
        model_instances[name] = AutoModelForCausalLM.from_pretrained(model_path)
        print(f"{name} model loaded successfully!")
    except Exception as e:
        print(f"Error loading {name} model: {e}")

print("All models loaded successfully!")

print(f"CUDA available: {torch.cuda.is_available()}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    selected_model = request.json.get('model', 'gpt2')  # Default to gpt2 if not specified
    
    tokenizer = tokenizers.get(selected_model)
    model = model_instances.get(selected_model)
    
    if not tokenizer or not model:
        return jsonify({'response': "Oops! Model not found. Please select a valid model."})
    
    try:
        prompt = f"Human: {user_message}\nAssistant:"
        inputs = tokenizer.encode(prompt, return_tensors="pt")
        
        outputs = model.generate(
            inputs, 
            max_length=150, 
            num_return_sequences=1, 
            temperature=0.7,
            no_repeat_ngram_size=2,
            top_k=50,
            top_p=0.95,
            timeout=60
        )
        
        bot_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        bot_response = bot_response.split("Assistant:")[-1].strip()
        
    except Exception as e:
        print(f"Error in generating response: {e}")
        bot_response = "Oops! Mujhe samajh nahi aaya. Phir se pucho."
    
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
