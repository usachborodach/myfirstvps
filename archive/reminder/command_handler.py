import logger
from postpone import postpone
from send_to_tg_and_wekan import send_to_tg_and_wekan
from delete import delete

def command_handler():
    input_str = input()
    try:
        if input_str == "exit":
            logger.log_debug("User exited the application")
            exit()
        input_str = input_str.split()
        if len(input_str) < 2:
            logger.log_debug("Invalid command format")
            return
        command, index = input_str[0], int(input_str[1])
        if command == "done":
            logger.log_debug(f"User marked reminder {index} as done")
            postpone(index)
        elif command == "send":
            logger.log_debug(f"User manually sent reminder {index}")
            send_to_tg_and_wekan(index)
        elif command == "del":
            logger.log_debug(f"User deleted reminder {index}")
            delete(index)
        else:
            logger.log_warning(f"Unknown command: {command}")
    except Exception as e:
        logger.log_error(f"Error in command handler '{input_str}': {str(e)}")