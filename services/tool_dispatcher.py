from tools.weather_tool import get_weather
from tools.datetime_tool import get_current_datetime

TOOL_REGISTRY = {
    "get_weather": get_weather,
    "get_current_datetime": get_current_datetime
}



def execute_tool(tool_use):

    tool = TOOL_REGISTRY.get(
        tool_use.name
    )
    if not tool:
        raise Exception(
            f"Tool not found {tool_use.name}"
        )
    
    return tool(
        **tool_use.input
    )