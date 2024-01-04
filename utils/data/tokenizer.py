import torch 
import pandas as pd
from typing import List
from transformers import T5Tokenizer, T5ForConditionalGeneration

from ipdb import set_trace

from tqdm import tqdm
tqdm.pandas()

class TextTokenizer():
    def __init__(self) -> None:
        # Initialize the T5 tokenizer and model
        self.en_tokenizer = T5Tokenizer.from_pretrained('t5-small')
        self.ja_tokenizer = T5Tokenizer.from_pretrained('sonoisa/t5-base-japanese')
        self.encode_model = T5ForConditionalGeneration.from_pretrained('t5-small')
        self.max_source_length = 256

    def tokenize_en(self, text: List[str]):
        '''
        Args: 
            text: list(string)
        '''
        return self.en_tokenizer(text,
                        max_length=self.max_source_length,
                        truncation=True,
                        padding = "max_length",
                        return_tensors='pt')

    def tokenize_ja(self, text: List[str]):
        '''
        Args: 
            text: list(string)
        '''
        if isinstance(text, str):
            text = [text]
        try:
            return self.ja_tokenizer(text,
                        max_length=self.max_source_length,
                        truncation=True,
                        padding = "max_length",
                        return_tensors='pt')
        except:
            set_trace()

    def detokenize_en(self, feature: torch.Tensor):
        '''
        Args: 
            feature (torch.Tensor): SINGLE tensor that represents the feature
        '''
        return self.en_tokenizer.decode(feature)
    
    def detokenize_ja(self, feature: torch.Tensor):
        '''
        Args: 
            feature (torch.Tensor): SINGLE tensor that represents the feature
        '''
        return self.ja_tokenizer.decode(feature)
    
    def detokenize_en_batch(self, features: torch.Tensor):
        '''
        Args: 
            features (torch.Tensor): BATCH tensor that represents the features
        '''
        return [self.detokenize_en(feature) for feature in features]
    
    def detokenize_ja_batch(self, features: torch.Tensor):
        '''
        Args: 
            features (torch.Tensor): BATCH tensor that represents the features
        '''
        return [self.detokenize_ja(feature) for feature in features]
    
    