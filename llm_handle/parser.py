import re
def extract_cmd(response:str) -> str:
    """
    Process the response from chatgpt_wrapper, and extract the command for the bot.
    
    Parameters
    ----------
    response: str
        The response from chatgpt_wrapper.

    Returns
    ----------
    command: str
        The command for the bot.
    """
    # The response from chatgpt_wrapper is a string.
    # The command is wrapped in ```<command>```, and our goal is to extract the command.
    try:
        code_count = response.count("```")
        if code_count == 0:
            return False
        elif code_count % 2 == 1:
            raise ValueError("The number of ``` is not even.")
        # Extract the command from the response.
        result_list = re.findall(r"```(.+?)```", response, re.DOTALL)
        if len(result_list) > 1:
            raise ValueError("More than one command is found.")
    except AttributeError:  # Nonetype, nothing found
        return False
    
    result = result_list[0]
    if result[0] == "\n": # If the command starts with a newline, remove it.
        result = result[1:]
    
    return result


