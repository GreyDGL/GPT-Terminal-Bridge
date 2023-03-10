from chatgpt_wrapper import ChatGPT
from llm_handle.parser import extract_cmd
from task_handle.cmd_execution import execute_cmd
import os

def __main__():
    bot = ChatGPT()
    response = bot.ask("Can you give me a sample command in Mac terminal for checking the user names? Please give me the code directly.")
    sample_response = """
    Certainly! To list all user names on a Mac using the terminal, you can use the `dscl` command with the `list` option for the `/Users` node. Here's the command:
    ```
    dscl . list /Users | grep -v '^_'
    ```

    This will output a list of all user accounts on the system, excluding any system accounts that start with an underscore.
    """
    # print("The response is:", response)
    command = extract_cmd(str(response))
    print("The command is:", command)

    # execute the command in the terminal
    output = execute_cmd(command)
    print("The output is:\n", output)
    # Ideally, the output should be:
    """
    daemon
    uname
    nobody
    root"""

    # delete the session in the end
    bot.delete_conversation()



