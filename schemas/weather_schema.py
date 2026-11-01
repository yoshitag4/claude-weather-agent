from anthropic.types import ToolParam
weather_schema = ToolParam(
    {
        "name": "get_weather",
        "description": "Returns the current weather of one or more cities.",
        "input_schema": {
            "type": "object",
            "properties": {
                "cities": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            },
            "required": ["cities"]
        }
    }
)