import torch 
from torch.utils.data import Dataset
from utils.data.tokenizer import TextTokenizer
import pandas as pd
import os

class CardDataset(Dataset):
    def __init__(self, source):
        # Data can be path or dataframe
        if isinstance(source, str) or isinstance(source, os.PathLike):
            self.data = pd.read_csv(source)
        else:
            self.data = source
        
        assert isinstance(self.data, pd.DataFrame), "Data must be either path or dataframe"
            
        self.tokenizer = TextTokenizer()

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        src_text = self.data.iloc[idx]["ja"]
        tgt_text = self.data.iloc[idx]["en"]

        # Tokenize source and target texts
        tokenized_inputs = self.tokenizer.tokenize_ja(src_text)
        tokenized_outputs = self.tokenizer.tokenize_en(tgt_text)
        
        return {
            "input_ids": tokenized_inputs["input_ids"].squeeze(),
            "attention_mask": tokenized_inputs["attention_mask"].squeeze(),
            "labels": tokenized_outputs["input_ids"].squeeze(),
        }