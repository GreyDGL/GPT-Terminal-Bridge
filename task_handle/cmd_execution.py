
import os, subprocess

def execute_cmd(cmd:str) -> str:
    """
    Execute the command in the mac terminal.
    
    Parameters
    ----------
    cmd: str
        The command to be executed.
    
    Returns
    ----------
    output: str
        The output of the command.
    """
    try:
        # execute the command in the system terminal
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr = None, shell=True)
        output = ""
        # some tools may take time to execute. Wait until the output is finished.
        while True:
            line_output = p.stdout.readline()
            if line_output:
                output += line_output.decode("utf-8")
            if line_output == b'' and p.poll() is not None:
                break

        return output
    except Exception as e:
        print("Error in executing the command:", e)
        return None