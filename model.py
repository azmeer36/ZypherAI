import time
import random
from typing import Dict

# Mock model function

def mock_model_predict(input_data: str) -> Dict[str,str]:
    # Simulate the processing time     
    time.sleep(random.randint(8, 15))
    
    # Return a random result
    result = str(random.randint(100, 10000))
    output = {"input": input_data, "result": result}
    return output