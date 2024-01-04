import sys
import os

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

from transformers import T5ForConditionalGeneration
from utils.data.dataset import CardDataset
from transformers import Trainer, TrainingArguments


# Load the pre-trained model
model_name = "t5-base"
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Load checkpoint from path 
# model_name = "t5-base"
# model = T5ForConditionalGeneration.from_pretrained(model_name, state_dict=torch.load('checkpoint.pth'))

# Load the dataset
train_dataset = CardDataset('data/train_261203.csv')
val_dataset = CardDataset('data/test_261203.csv')


# Define optimizer and learning rate
optimizer = "adam"  
learning_rate = 1e-4  

# Training arguments with optimizer and learning rate settings
training_args = TrainingArguments(
    output_dir="./results",
    learning_rate=learning_rate,
    per_device_train_batch_size=16,
    num_train_epochs=60,
    weight_decay=0.01,  # Optional: Specify weight decay if needed
    logging_dir="./logs",
    logging_steps=1000,
    evaluation_strategy="steps",
    eval_steps=1000,
)

# Initialize the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)


# Start training
trainer.train()
