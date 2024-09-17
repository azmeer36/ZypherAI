from marshmallow import Schema, fields


# Marshmallow Schemas for validation and documentation
class AsyncModeHeaderSchema(Schema):
    """Schema to define the Async-Mode header"""
    async_mode = fields.Bool(
        required=False,
        description="If set to true, the task will be processed asynchronously.",
        data_key='Async-Mode',
    )

class PredictionInputSchema(Schema):
    input = fields.Str(required=True, example="Sample input data for the model")

class PredictionResponseSchema(Schema):
    input = fields.Str()
    result = fields.Str()
    
class AsyncPredictionSchema(Schema):
    prediction_id = fields.Str(required=True)
    output = fields.Nested(PredictionResponseSchema, required=True)

class AsyncResponseSchema(Schema):
    message = fields.Str()
    prediction_id = fields.Str()
    
class ErrorResponseSchema(Schema):
    error = fields.Str()