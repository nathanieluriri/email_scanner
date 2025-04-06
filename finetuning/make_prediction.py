
def predict_reason(action_text):
    import json
    prediction=None
    action_text= ' '.join(action_text.split())
    with open(r'./finetuning/training-data.json','r') as file:
        data_store= json.load(file)
        
    for data in data_store:
        if data['action'].strip() == action_text.strip():
            prediction= data
    
    
    if prediction==None:
        from transformers import T5Tokenizer, T5ForConditionalGeneration
        # Load the fine-tuned model and tokenizer
        model_name = r"./finetuning/t5_finetuned"  # Path to your saved model
        tokenizer = T5Tokenizer.from_pretrained(model_name)
        model = T5ForConditionalGeneration.from_pretrained(model_name)

        input_text = f"action: {action_text}"
        input_ids = tokenizer(input_text, return_tensors="pt").input_ids

        

        outputs = model.generate(
            input_ids, 
            max_length=64, 
            num_beams=5,  # Use beam search for better results
            top_k=50,
            temperature=1.0 
        )


        prediction = tokenizer.decode(outputs[0], skip_special_tokens=True)
        def parse_prediction(prediction,input_t):
            fields = prediction.split(", ")
            result = {}
            key,value = input_t.split(':')
            result[key] = value.strip()
            for field in fields:
                key, value = field.split(": ")
                result[key] = value

            return result
        
        prediction = parse_prediction(prediction=prediction,input_t=input_text)

    return prediction





