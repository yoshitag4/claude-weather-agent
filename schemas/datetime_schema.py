from anthropic.types import ToolParam


datetime_schema = ToolParam(
    {
        "name": "get_current_datetime",
        "description": "Returns the current date and time.",
        "input_schema": {
            "type": "object",
            "properties": {
                "date_format": {
                    "type": "string",
                    "description": "Python datetime format string",
                    "default": "%Y-%m-%d %H:%M:%S"
                },
                "timezone": {
                    "type": "string",
                    "description": (
                        "IANA timezone name for the location the user asked about "
                        "(e.g. 'America/New_York' for New York, 'Asia/Kolkata' for India, "
                        "'Europe/London' for London). Infer this from any city/country "
                        "mentioned in the user's question. Omit to use the system's local time."
                    )
                }
            }
        }
    }
)