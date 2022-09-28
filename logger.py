import atexit
import datetime


class AnsiCodes:
    """
    Some useful Ansi codes to use in the console.
    Use reset do fallback to default styles.
    Commands from the same group will be overwritten
    """

    # colors
    black = "\u001b[30m"
    gray = "\u001b[38;5;240m"
    red = "\u001b[31m"
    green = "\u001b[32m"
    yellow = "\u001b[33m"
    blue = "\u001b[34m"
    magenta = "\u001b[35m"
    cyan = "\u001b[36m"
    white = "\u001b[37m"

    # backgrounds
    b_black = "\u001b[40;1m"
    b_red = "\u001b[41;1m"
    b_green = "\u001b[42;1m"
    b_yellow = "\u001b[43;1m"
    b_blue = "\u001b[44;1m"
    b_magenta = "\u001b[45;1m"
    b_yan = "\u001b[46;1m"
    b_white = "\u001b[47;1m"

    # decorations
    bold = "\u001b[1m"
    underline = "\u001b[4m"
    reversed = "\u001b[7m"

    reset = "\u001b[0m"


class Log:
    """
    Use this custom logger to have a beautiful logging experience.
    Supports multiple arguments to be formatted to string automatically.
    Change color for single messages and separate your arguments witch customisable strings.
    Use markdowns for fancy formats.
    Two logger documents your output for the last session and with history.
    Use in productive space with different logging levels, for example errors only.
    """

    lvl_info = 1
    lvl_debug = 2
    lvl_warn = 3
    lvl_error = 4

    # Current logging level
    lvl = lvl_info

    # specify the symbol witch will be replaced by an ansi tag (only single symbols)
    markdown_dict = {
        "*": AnsiCodes.bold,
        "_": AnsiCodes.underline
    }

    session_writer = None
    global_writer = None

    def __init__(self, log_global: bool = True, log_session=True, path="logs"):
        """
        A custom Logger with many functions for styled logging

        Parameters
        ----------
        log_global: bool
            default true; if true, the historical logger will be activated
        log_session: bool
            default true; if true, the session will be logged to a file. Warning, the last session will be overwritten
        path: str
            default 'logs'; the relative or absolut path to the logging folder

        Returns
        -------
        None
        """
        if log_global:
            self.global_writer = open(path + "/log.log", "a")
        if log_session:
            self.session_writer = open(path + "/session.log", "w")
        self.info("--------Program start--------")
        atexit.register(self.on_exit)

    def on_exit(self):
        """
        Triggered if the program ends. Clarified the end in the logging history for better overview

        Returns
        -------
        None
        """
        self.info("--------Program end--------")
        if self.global_writer is not None:
            self.global_writer.close()
        if self.session_writer is not None:
            self.session_writer.close()

    def set_logging_lvl(self, lvl: int):
        """
        Sets the logging level to the given level

        Parameters
        ----------
        lvl: int
            The new logging level (use only class fields)

        Returns
        -------
        None
        """
        self.lvl = lvl

    def print_to_console(self, msg: str, lvl: int, *args, obj=None, join=" ", color=None):
        """
        Print the given message to the console with customisable styles.
        You can use markdowns, colors and object references.

        Parameters
        ----------
        msg: str
            The string witch will be printed to the console
        lvl: int
            The logging level, witch will be uses (Use class fields only)
        args: any
            Other arguments witch will append to the message as a string
        obj: any
            default None; Reference to an object for easy find code position and differentiate objects
        join: str
            default ' '; The string, witch separates multiple arguments
        color: str
            default None; Custom color for this message.

        Returns
        -------
        None
        """
        output = AnsiCodes.gray  # Metadata displayed in gray
        active_ansi = [AnsiCodes.gray]
        if obj is not None:  # with object reference the logging messages is about 4 lines
            output += "-----\n"
        output += datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S.%f")  # timestamp at begin of message
        output += " ~ "
        # Adding logging level and set color
        if lvl == self.lvl_info:
            output += "INFO "
        elif lvl == self.lvl_debug:
            output += AnsiCodes.white + "DEBUG"
            active_ansi = [AnsiCodes.white]
        elif lvl == self.lvl_warn:
            output += AnsiCodes.yellow + "WARN "
            active_ansi = [AnsiCodes.yellow]
        elif lvl == self.lvl_error:
            output += AnsiCodes.red + "ERROR"
            active_ansi = [AnsiCodes.red]
        else:
            output += "UNKNO"
        output += " ~ "
        if color is not None:  # the user can set a custom color
            active_ansi = [color]
            output += color
        if obj is not None:
            output += AnsiCodes.gray
            output += str(obj)
            for ansi in active_ansi:
                output += ansi
            output += "\n"
        output += self.markdown_to_ansi(msg, active_ansi)  # The actual message, styled with markdowns
        for sub_message in args:
            output += join + self.markdown_to_ansi(str(sub_message), active_ansi)
        if obj is not None:
            output += AnsiCodes.gray + "\n-----" + AnsiCodes.reset
        print(output)

    def write_to_file(self, msg: str, lvl: int, *args, obj=None, join=" "):
        """
        Writes the given message to the logging files.
        Styling components will be automatically removed

        Parameters
        ----------
        msg: str
            The string witch will be printed to the console
        lvl: int
            The logging level, witch will be uses (Use class fields only)
        args: any
            Other arguments witch will append to the message as a string
        obj: any
            default None; Reference to an object for easy find code position and differentiate objects
        join: str
            default ' '; The string, witch separates multiple arguments

        Returns
        -------
        None
        """
        output = datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S.%f")
        output += " ~ "
        if lvl == self.lvl_info:
            output += "INFO "
        elif lvl == self.lvl_debug:
            output += "DEBUG"
        elif lvl == self.lvl_warn:
            output += "WARN "
        elif lvl == self.lvl_error:
            output += "ERROR"
        else:
            output += "UNKNO"
        output += " ~ "
        if obj is not None:
            output += str(obj) + " ~ "
        output += self.remove_markdowns(msg)
        for sub_message in args:
            output += join + self.remove_markdowns(sub_message)

        output += "\n"

        if self.global_writer is not None:
            self.global_writer.write(output)
        if self.session_writer is not None:
            self.session_writer.write(output)

    def markdown_to_ansi(self, msg, ongoing_ansi: []) -> str:
        """
        Exchange markdowns to interpretable ansi codes.
        Use [nmd] at the beginning of the message to deactivate this option

        Parameters
        ----------
        msg: str
            The string witch will be edited
        ongoing_ansi: str[]
            Multiple ansi codes witch continues after end of markdown

        Returns
        -------
        None
        """
        if msg[0:5] == "[nmd]":
            return msg[5:]

        open_tags = []
        message = ""
        for char in msg:
            founded = False
            if char in self.markdown_dict:
                founded = True
                if char in open_tags:
                    message += AnsiCodes.reset
                    for ansi in ongoing_ansi:
                        message += ansi
                    open_tags.remove(char)
                else:
                    message += self.markdown_dict[char]
                    open_tags.append(char)
            if not founded:
                message += char
        return message

    def remove_markdowns(self, msg: str):
        """
        Removes markdowns. Use [nmd] at the beginning of the message to deactivate this method

        Parameters
        ----------
        msg: str
            The string witch will be printed to the console

        Returns
        -------
        None
        """
        if msg[0:5] == "[nmd]":
            return msg[5:]

        message = ""
        for char in msg:
            if char not in self.markdown_dict:
                message += char
        return message

    def info(self, msg, *args, obj=None, join=" ", color=None):
        """
        Logs a low level message

        Parameters
        ----------
        msg: str
            The message to be logged
        *args: any
            Multiple messages can be given to this function, all arguments will be handled as string
        obj: any
            default None; a reference to an object to find code position in easy way
        join: str
            default ' '; the string witch separates multiple arguments
        color: str
            default None; the color of the message

        Returns
        -------
        None
        """
        if self.lvl_info < self.lvl:
            return

        self.print_to_console(msg, self.lvl_info, *args, obj=obj, join=join, color=color)
        self.write_to_file(msg, self.lvl_info, *args, obj=obj, join=join)

    def debug(self, msg, *args, obj=None, join=" ", color=None):
        """
        Logs a message to be shown in debug mode

        Parameters
        ----------
        msg: str
            The message to be logged
        *args: any
            Multiple messages can be given to this function, all arguments will be handled as string
        obj: any
            default None; a reference to an object to find code position in easy way
        join: str
            default ' '; the string witch separates multiple arguments
        color: str
            default None; the color of the message

        Returns
        -------
        None
        """
        if self.lvl_debug < self.lvl:
            return

        self.print_to_console(msg, self.lvl_debug, *args, obj=obj, join=join, color=color)
        self.write_to_file(msg, self.lvl_info, *args, obj=obj, join=join)

    def warn(self, msg, *args, obj=None, join=" ", color=None):
        """
        Logs a warning message to indicate that an error has occurred, but the program continues to run.

        Parameters
        ----------
        msg: str
            The message to be logged
        *args: any
            Multiple messages can be given to this function, all arguments will be handled as string
        obj: any
            default None; a reference to an object to find code position in easy way
        join: str
            default ' '; the string witch separates multiple arguments
        color: str
            default None; the color of the message

        Returns
        -------
        None
        """
        if self.lvl_warn < self.lvl:
            return

        self.print_to_console(msg, self.lvl_warn, *args, obj=obj, join=join, color=color)
        self.write_to_file(msg, self.lvl_info, *args, obj=obj, join=join)

    def error(self, msg, *args, obj=None, join=" ", color=None):
        """
        Logs a critical error that may interrupt program execution.

        Parameters
        ----------
        msg: str
            The message to be logged
        *args: any
            Multiple messages can be given to this function, all arguments will be handled as string
        obj: any
            default None; a reference to an object to find code position in easy way
        join: str
            default ' '; the string witch separates multiple arguments
        color: str
            default None; the color of the message

        Returns
        -------
        None
        """
        if self.lvl_error < self.lvl:
            return

        self.print_to_console(msg, self.lvl_error, *args, obj=obj, join=join, color=color)
        self.write_to_file(msg, self.lvl_info, *args, obj=obj, join=join)


# Import this Variable for simple access to the logger. Do not instantiate multiple Objects!
Console = Log()

if __name__ == "__main__":
    Console.info("Hello to my logger!")
    Console.debug("The logger supports many functions", "like appending arguments", join=", ")
    Console.warn("different logging levels with different colors")
    Console.error("and two loggers, for historical logging and session logging")
    Console.debug("You can also refer to an objects instance to find the logging message in your code", obj=Console)
    Console.warn("Or you change the color of a message and use *markdowns* to _decorate_ your text",
                 color=AnsiCodes.blue)
    Console.debug("[nmd]Of course you *can deactivate _____ the markdown___ formatting")
