from cmd_dispatcher import CmdDispatcher  
from terminal_screen import TerminalScreen

if __name__ == '__main__':
    cmd_dispatcher = CmdDispatcher('commands/') 

    def command_handler(command, dispatcher, terminal: TerminalScreen): 
        return(dispatcher.dispatch(command, "commands", terminal))
        return f"Received command: {command}"

    terminal = TerminalScreen("commands")
    terminal.set_command_handler(lambda command: command_handler(command, cmd_dispatcher, terminal))  # Pass cmd_dispatcher to command_handler
    terminal.run()  
    


