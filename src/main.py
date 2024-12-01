from scripts import a_make_fred, b_train_models
from config.params import make_fred, train_models
import time

if __name__ == '__main__':
    
    if make_fred:
        
        print("Building FRED dataset...")
        
        make_fred_start = time.time()
        a_make_fred.execute()
        make_fred_end = time.time()
        
        print(f"Time taken to build dataset: {(make_fred_end - make_fred_start)/60} minutes")
        
    if train_models:
        
        print("Training models...")
        
        train_models_start = time.time()
        b_train_models.execute()
        train_models_end = time.time()
        
        print(f"Models trained in {(train_models_end - train_models_start) / 60:.2f} minutes")