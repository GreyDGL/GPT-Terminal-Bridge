from chatgpt_wrapper import ChatGPT
from task_handle.cmd_execution import execute_cmd
import os, logging, re
from .custom_exceptions import NoCodeFromResponseException


class chatGPTTemplate():
    """
    A template for the chatGPT task.
    It contains the basic functions that are required for the task.
    """

    def __init__(self, bot_session, init_script=None):
        """
        Initialize the by taking the session
        The bot session is a standard chatgpt_wrapper bot session. 
        More details at https://github.com/mmabrouk/chatgpt-wrapper

        Parameters:

        Variables:

        Returns:

        """

        ## Default storage variable
        self._chat_history = []  # Ask, Answer, Ask, Answer, ...
        self.logger = logging.getLogger()
        logging.basicConfig(level=logging.INFO)

        ## Define all the variables
        self._bot_session = bot_session
        self._init_script = init_script
        self._prefix = None
        self._exception_ask = {}
    
    def _extract_command(self, response: str) -> str:
        """
        This function is used to extract the command from the response.
        Parameters:
            response (str): The response from the bot.
        Returns:
            command (str): The command to be executed.
        """
        try:
            code_count = response.count("```")
            if code_count == 0:
                raise NoCodeFromResponseException("No code is found in the response.")
            elif code_count % 2 == 1:
                raise ValueError("The number of ``` is not even.")
            # Extract the command from the response.
            result_list = re.findall(r"```(.+?)```", response, re.DOTALL)
            if len(result_list) > 1:
                raise ValueError("More than one command is found.")
        except Exception:  # Nonetype, nothing found
            raise NoCodeFromResponseException("No code is found in the response.")
        
        result = result_list[0]
        if result[0] == "\n": # If the command starts with a newline, remove it.
            result = result[1:]
        
        return result

    def _cmd_wrapper(self, cmd: str) -> str:
        """
        This function is used to wrap the command execution function.
        Parameters:
            cmd (str): The command to be executed.
        Returns:
            output (str): The output of the command, or an Exception
        """
        # the possible types of exceptions
        output = execute_cmd(cmd)
        return output
        
    
    def _update_init_script(self, init_script: str):
        """
        This function is used to update the initialization script.
        Parameters:
            init_script (str): The initialization script.
        Returns:
        """
        self._init_script = init_script

    def _update_prefix(self, prefix: str):
        """
        This function is used to update the prefix.
        Parameters:
            prefix (str): The prefix to be appended.
        Returns:
        """
        self._prefix = prefix

    def _append_prefix(self, question: str, prefix: str):
        """
        This function is used to append the prefix to the question to ask the bot.
        Parameters:
            prefix (str): The prefix to be appended.
        Returns:
        """
        return prefix + question
    

    ########## Implementations ##########

    def initialize(self):
        """
        This function is called when the task is initialized.
        This is used to provide the necessary information for the task.
        """
        if self._init_script is not None:
            self._bot_session.ask(self._init_script)
    
    def ask(self, question: str, need_prefix = False) -> str:
        """
        Wrap the default bot ask function.
        Parameters:
            question (str): The question to ask the bot.
        Returns:
            response (str): The response from the bot.
        """
        if need_prefix:
            question = self._append_prefix(question, self._prefix)
        try:
            self.logger.info("Asking the question: \n%s \n------------" % question)
            response = self._bot_session.ask(question)
            self.logger.info("The response is: \n%s \n------------" % response)
            self._chat_history.append(question)
            self._chat_history.append(response)
            return response
        except Exception as e:
            print("Error in asking the question:", e)
            return None
    
    def exception_ask(self, question: str) -> str:
        """
        This function is used to ask the bot when an exception is raised.
        Parameters:
            question (str): The question to ask the bot.
        Returns:
            response (str): The response from the bot.
        """
        if self._exception_ask is not None:
            return self.ask(self._exception_ask)
        else:
            return None
    
    def run(self):
        """
        The function with the main logic. This should be overwritten in the task execution.
        """
        print("Please override the run function!")
        pass