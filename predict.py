from flask_smorest import Blueprint
from flask import request, jsonify, Response
from model import mock_model_predict
import threading
import uuid
import queue

blp = Blueprint("predict", __name__, description="Prediction operations")

# Initialize task queue and predictions dictionary
task_queue = queue.Queue() # For lining up async tasks
predictions = {} # Temporary storage for async prediction results



# Background worker thread
def worker() -> None:
    while True:
        prediction_id, input_data = task_queue.get()
        if prediction_id is None:
            break
        prediction = mock_model_predict(input_data)
        predictions[prediction_id] = prediction
        task_queue.task_done()

# Start worker thread
threading.Thread(target=worker, daemon=True).start()

@blp.route("/predict", methods=["POST"])
@blp.response(200, description="Returns the prediction results or ID for async requests")
def predict() -> Response:
    
    # Perform prediction on synchronous or asynchronous requests.
    
    data = request.get_json()
    if data is None: # Return Error if not in JSON format
        return jsonify({"error": "Content Type is not JSON"}), 404

    if 'input' not in data : # Return error if input not included
        return jsonify({"error": "No input data provided"}), 400


    if not isinstance(data['input'], str):
        return jsonify({"error": "Input data should be string"}), 405
        
    input_data = data['input']

    async_mode = request.headers.get('Async-Mode')
    # Asynchronous prediction
    if async_mode:
        prediction_id = str(uuid.uuid4())  # Generate unique ID  # No need to check against prev generated IDs
        
        predictions[prediction_id] = None  # Reserve the ID
        response = {
            "message": "Request received. Processing asynchronously.",
            "prediction_id": prediction_id
        }
        task_queue.put((prediction_id, input_data))  # Queue the task
        return jsonify(response), 202

    # Synchronous prediction
    prediction = mock_model_predict(input_data)
    return jsonify(prediction), 200



@blp.route("/predict/<string:prediction_id>", methods=["GET"])
@blp.response(200, description="Fetches the prediction results for async requests")
def get_prediction_result(prediction_id: str) -> Response:
    
    # Fetch results of asynchronous predictions 
    
    if prediction_id not in predictions: # Pred ID is incorrect
        return jsonify({"error": "Prediction ID not found"}), 404 

    result = predictions[prediction_id]
    if result is None: # Result not ready
        return jsonify({"error": "Prediction is still being processed."}), 400

    # Return result if ready
    return jsonify({"prediction_id": prediction_id, "output": result}), 200
