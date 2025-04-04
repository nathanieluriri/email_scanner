import json
import pandas as pd
from datasets import Dataset, DatasetDict
from transformers import (
    T5Tokenizer,
    T5ForConditionalGeneration,
    Trainer,
    TrainingArguments,
    DataCollatorForSeq2Seq,
)



# 1. Load your JSON data
with open(r"C:\\Users\Mr Dashi\Downloads\email_scanner\data\actionAUGUST.json", "r") as f:
    data = json.load(f)

# 2. Convert the JSON list to a Pandas DataFrame
df = pd.DataFrame(data)

# Fix typo in column name if necessary
if "maintenenance" in df.columns:
    df.rename(columns={"maintenenance": "maintenance"}, inplace=True)

# 3. Create input and target strings
def create_example(row):
    input_text = f"action: {row['action']}"
    target_text = (
        f"reason: {row['reason']}, "
        f"maintenance: {row['maintenance']}, "
        f"category: {row['category']}, "
        f"equipment: {row['equipment']}"
    )
    return {"input_text": input_text, "target_text": target_text}

examples = df.apply(create_example, axis=1)
df_examples = pd.DataFrame(list(examples))




# 4. Convert DataFrame to a Hugging Face Dataset
dataset = Dataset.from_pandas(df_examples)


# 5. Split the dataset into train & validation sets
split_dataset = dataset.train_test_split(test_size=0.3)
train_dataset = split_dataset["train"]
val_dataset = split_dataset["test"]


# 6. Load the T5 tokenizer and model
model_name = "t5-base"  # Change to "t5-base" for better performance
tokenizer = T5Tokenizer.from_pretrained(model_name, legacy=False)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# 7. Preprocess dataset (Tokenize inputs & targets)
def preprocess_function(examples):
    model_inputs = tokenizer(
        examples["input_text"], max_length=64, padding="max_length", truncation=True
    )
    labels = tokenizer(
        examples["target_text"], max_length=64, padding="max_length", truncation=True
    )
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

tokenized_train = train_dataset.map(preprocess_function, batched=True, remove_columns=train_dataset.column_names)
tokenized_val = val_dataset.map(preprocess_function, batched=True, remove_columns=val_dataset.column_names)


# 8. Convert datasets to torch format
tokenized_train.set_format(type="torch", columns=["input_ids", "attention_mask", "labels"])
tokenized_val.set_format(type="torch", columns=["input_ids", "attention_mask", "labels"])

# # 9. Define training arguments

training_args = TrainingArguments(
    output_dir="./t5_finetuned",
    num_train_epochs=5,  # Increase epochs for better learning
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    evaluation_strategy="epoch",  # Evaluate on val set every epoch
    save_strategy="epoch",  # Save model every epoch
    logging_steps=10,
    save_total_limit=2,  # Keeps only the latest 2 checkpoints
    load_best_model_at_end=True,
    metric_for_best_model="loss",  # Saves best model based on loss
)

# 10. Use DataCollatorForSeq2Seq for padding
data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

# 11. Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_val,
    data_collator=data_collator,
   
)

# 12. Train the model
trainer.train()

# 13. Save fine-tuned model & tokenizer
trainer.save_model("./t5_finetuned")
tokenizer.save_pretrained("./t5_finetuned")
