from flask_smorest import Blueprint
from flask import request, jsonify, Response
from model import mock_model_predict
from schemas import PredictionInputSchema, PredictionResponseSchema, AsyncResponseSchema, ErrorResponseSchema, AsyncPredictionSchema
from schemas import AsyncModeHeaderSchema
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
@blp.arguments(PredictionInputSchema, location="json")
@blp.arguments(AsyncModeHeaderSchema, location="headers")
@blp.response(200, PredictionResponseSchema, description="Synchronous Request Response")
@blp.response(202, AsyncResponseSchema, description="Async Request Response ")
def predict(args, async_mode) -> Response:
    # Perform prediction on synchronous or asynchronous requests. 
    input_data = args['input']

    async_mode = request.headers.get('Async-Mode')
    # Asynchronous prediction
    if async_mode == 'true' or async_mode == 'True':
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
@blp.response(200, AsyncPredictionSchema)
@blp.response(400, ErrorResponseSchema)
@blp.response(404, ErrorResponseSchema)
def get_prediction_result(prediction_id: str) -> Response:
    
    # Fetch results of asynchronous predictions 
    if prediction_id not in predictions: # Pred ID is incorrect
        return jsonify({"error": "Prediction ID not found"}), 404 

    result = predictions[prediction_id]
    if result is None: # Result not ready
        return jsonify({"error": "Prediction is still being processed."}), 400

    # Return result if ready
    return jsonify({"prediction_id": prediction_id, "output": result}), 200
