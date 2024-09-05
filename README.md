# Flask Web app for ML Inferencing in ZypherAI

## Project Overview

This project is a simple Flask web application that simulates synchronous and asynchronous machine learning predictions using Python's built-in `queue.Queue` for task management. Users can submit a prediction request to the `/predict` endpoint, and the system processes the task in the background. A separate worker processes tasks from the queue. The application also includes endpoints for retrieving the results of predictions.

## Approach

The approach used for managing asynchronous tasks leverages Python’s built-in `queue.Queue` and multithreading. We chose this method to keep the system lightweight and avoid introducing external dependencies like Redis or Celery. This makes the application easier to deploy in environments where setting up distributed systems may not be necessary.

The key components include:
- **Flask**: Web framework to handle HTTP requests.
- **`queue.Queue`**: For managing asynchronous task submission.
- **Multithreading**: For background task processing with worker threads.


## Logic Behind the Worker Function and Queueing

### Task Queueing:
When a prediction request is submitted to the `/predict` endpoint, the application pushes a new task into the queue (`queue.Queue`). The task includes the `prediction_id` and the input data. The queue acts as a buffer, ensuring that incoming tasks are stored and processed asynchronously by the worker(s) in the background. This design allows the Flask app to return an immediate response to the client without waiting for the prediction task to complete.

Here is how task queueing works:
1. **Task Submission**: When the user submits a post request to `/predict` with the header Async-Mode = True, a new task is created and placed into the task queue using `task_queue.put()`.
2. **Task Structure**: Each task is represented as a tuple containing:
   - `prediction_id`: A unique ID that identifies the prediction task.
   - `input_data`: The input data for the prediction.
   
### Worker Function:
The worker function is responsible for consuming tasks from the queue and processing them in the background. It continuously listens for new tasks in the queue using `task_queue.get()` and processes them. After the worker completes processing a task (e.g., simulating the prediction), it stores the result in an in-memory dictionary called `predictions`.

Key points about the worker function:
1. **Infinite Loop**: The worker function runs in an infinite loop (`while True`) to continuously process tasks from the queue.
2. **Task Retrieval**: The worker retrieves tasks from the queue using `task_queue.get()`. If no tasks are available, the worker will wait (block) until a new task arrives.
3. **Task Processing**: Once a task is retrieved, the worker simulates processing the task by calling a function like `mock_model_predict(input_data)`, which simulates the prediction process.
4. **Result Storage**: After processing, the worker stores the result in the `predictions` dictionary using the `prediction_id` as the key.
5. **Task Acknowledgment**: After successfully processing the task, the worker calls `task_queue.task_done()` to signal that the task has been completed. This is crucial for tracking task completion when using `queue.join()`.


## Optimizing Docker Image Size and Config:
The Docker image was optimized for size and performance by:

1. **Using a Smaller Base Image**: The base image used is python:3.10-alpine. This is a lightweight image that includes only the essential components of Python.
2. **Avoiding Cache in Pip Installation**: The --no-cache-dir option was used with pip install to ensure that no package installation caches are stored in the final image, further reducing the size.
3. **Using .dockerignore**: This file ensures that unneccessary files and directories are ignored when building the docker image, hence making it lighter.
4. **Using Multi-Stage Builds**: Although I did try using multistage build due to the app being simple and not having enough dependencies to leave in the build stage the difference in image size was not much. However for more complex apps this would still be a useful tool to reduce image size

  
## Project Structure
  ```bash
  Sych-SDE/
  ├── app.py              # Main Flask app and routing
  ├── predict.py          # Blueprint for predict endpoints
  ├── model.py            # Mock ML predict function
  ├── Dockerfile          # Dockerfile for containerization
  ├── requirements.txt    # Dependencies
  ├── README.md           # Project documentation
  ```

## Instructions to Run

### Prerequisites

- **Python 3.x**: Ensure Python is installed.
- **Docker**: Ensure Docker is installed.

### Local Development

1. **Download/Clone the Repository**:
2. **Set up the virtual environment (optional but recommended)**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
4. **Run the Flask app**:
   ```bash
   flask run

### Docker
1. **Build the Docker image**:
   ```bash
   docker build -t sych_sde .
2. **Run the Docker container**:
   ```bash
   docker run -d -p 8080:8080 sych_sde

The app will be available at http://localhost:8080

## Making Requests
Refer to the API_documentation pdf for making requests or go to http://localhost:8080/swagger
P.S Did not have enough time to config swagger properly using schemas

## Assumptions:
1. Single Server Deployment: Since we’re using queue.Queue, we assume that the application will run on a single server instance. This approach doesn’t support scaling across multiple machines because Python’s queue.Queue is memory-bound to the local process.
2. No Persistent Task Storage: The task results are stored in memory, meaning if the server restarts, all pending tasks and results will be lost. This is acceptable for short-lived, stateless tasks but not ideal for production environments where durability is required.


## Alternative Approach (Not Pursued):
An alternative approach considered was using Celery(for background processing) and Redis/RabbitMQ(shared queue) for distributed task management:
- Celery: A more scalable task queue that works well in distributed environments.
- Redis: A distributed in-memory data structure store that would have served as the broker for Celery.

Even though we did not include this approach for the sake of simplicity, scaling across multiple machines requires us to use celery and Redis/RabbitMQ for a more suitable long-term and practical solution.


## Future Improvements:
- Switch to Celery and Redis/RabbitMQ instead of bult-in queue
- Integrate a database or Redis for persistent task storage to ensure that tasks and results survive server restarts.










   


