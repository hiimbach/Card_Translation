import os 
import sys
import yaml
import warnings
from typing import Union

import pandas as pd
from clearml import TaskTypes
from clearml.automation.controller import PipelineDecorator

warnings.filterwarnings("ignore")
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
                

@PipelineDecorator.component(return_values=["df_save_path"], 
                             packages='./requirements.txt',
                             cache=True,
                             task_type=TaskTypes.data_processing,
                             repo='.')
def crawling_step(cfg):
     from utils.data.data_crawling import crawling_card_ds
     
     # Configs to crawl data      
     first_id = cfg['first_id']
     last_id = cfg['last_id']
     prepared_data_path = cfg['prep_data_path']
     save_path = cfg['save_path']
     postfix = cfg['postfix']
     
     # Crawling
     df = crawling_card_ds(first=first_id, 
                              last=last_id, 
                              save_path=save_path, 
                              prep_data_path=prepared_data_path,
                              postfix=postfix)
     
     return df


@PipelineDecorator.component(return_values=["train_path", "test_path"], 
                             packages='./requirements.txt',
                             cache=True,
                             task_type=TaskTypes.data_processing,
                             repo='.')

def splitting_dataset_step(cfg, df: pd.DataFrame):
     from utils.data.data_prepare import split_dataset

     # Configs to split dataset
     save_path = cfg['save_path']
     test_split_rate = cfg['test_split_rate']
     postfix = cfg['postfix']
     
     # Splitting dataset
     train_path, test_path = split_dataset(df=df, 
                                           save_path=save_path, 
                                           test_split_rate=test_split_rate, 
                                           postfix=postfix)
     
     return train_path, test_path

@PipelineDecorator.pipeline(name="Data Pipeline", 
                            project="Ygo_translator", 
                            version="0.0.1",
                            add_pipeline_tags=True,
                            default_queue='default',
                            pipeline_execution_queue=None)
def executing_data_pipeline(cfg_path: Union[str, os.PathLike]):
     assert os.path.exists(cfg_path), f"Config file {cfg_path} does not exist."
     with open(cfg_path) as f:
          cfg = yaml.load(f, Loader=yaml.FullLoader)['data_pipeline']
          
     # Crawling step
     df = crawling_step(cfg['crawling'])
     train_path, test_path = splitting_dataset_step(cfg['splitting'], df)
     
     return train_path, test_path  
     

if __name__ == '__main__':
     # Run pipeline locally, comment this line if you want to run on ClearML server   
     PipelineDecorator.debug_pipeline()     
     
     # Start the pipeline execution logic.
     executing_data_pipeline(cfg_path='configs/data_pipeline_config.yml')

     print("===== Data pipeline completed =====")