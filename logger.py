import atexit
import datetime


class AnsiCodes:
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
    reset = "\u001b[0m"

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


class Log:
    lvl_info = 1
    lvl_debug = 2
    lvl_warn = 3
    lvl_error = 4

    lvl = lvl_info

    markdown_dict = {
        "*": AnsiCodes.bold,
        "_": AnsiCodes.underline
    }

    session_writer = None
    global_writer = None

    def __init__(self, log_global: bool = True, log_session=True, path="logs"):
        if log_global:
            self.global_writer = open(path + "/log.log", "a")
        if log_session:
            self.session_writer = open(path + "/session.log", "w")
        self.info("--------Program start--------")
        atexit.register(self.on_exit)

    def on_exit(self):
        self.info("--------Program end--------")
        if self.global_writer is not None:
            self.global_writer.close()
        if self.session_writer is not None:
            self.session_writer.close()

    def print_to_console(self, msg: str, lvl: int, *args, obj=None, join=" ", color=None):
        output = AnsiCodes.gray
        active_ansi = [AnsiCodes.gray]
        if obj is not None:
            output += "-----\n"
        output += datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S.%f")
        output += " ~ "
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
        if color is not None:
            active_ansi = [color]
            output += color
        if obj is not None:
            output += AnsiCodes.gray
            output += str(obj)
            for ansi in active_ansi:
                output += ansi
            output += "\n"
        output += self.markdown_to_ansi(msg, active_ansi)
        for sub_message in args:
            output += join + self.markdown_to_ansi(str(sub_message), active_ansi)
        if obj is not None:
            output += AnsiCodes.gray + "\n-----" + AnsiCodes.reset
        print(output)

    def write_to_file(self, msg: str, lvl: int, *args, obj=None, join=" "):
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
        if msg[0:5] == "[nmd]":
            return msg[5:]

        message = ""
        for char in msg:
            if char not in self.markdown_dict:
                message += char
        return message

    def info(self, msg, *args, obj=None, join=" ", color=None):
        if self.lvl_info < self.lvl:
            return

        self.print_to_console(msg, self.lvl_info, *args, obj=obj, join=join, color=color)
        self.write_to_file(msg, self.lvl_info, *args, obj=obj, join=join)

    def debug(self, msg, *args, obj=None, join=" ", color=None):
        if self.lvl_debug < self.lvl:
            return

        self.print_to_console(msg, self.lvl_debug, *args, obj=obj, join=join, color=color)
        self.write_to_file(msg, self.lvl_info, *args, obj=obj, join=join)

    def warn(self, msg, *args, obj=None, join=" ", color=None):
        if self.lvl_warn < self.lvl:
            return

        self.print_to_console(msg, self.lvl_warn, *args, obj=obj, join=join, color=color)
        self.write_to_file(msg, self.lvl_info, *args, obj=obj, join=join)

    def error(self, msg, *args, obj=None, join=" ", color=None):
        if self.lvl_error < self.lvl:
            return

        self.print_to_console(msg, self.lvl_error, *args, obj=obj, join=join, color=color)
        self.write_to_file(msg, self.lvl_info, *args, obj=obj, join=join)


Console = Log()

if __name__ == "__main__":
    Console.info("Hello to my logger!")
    Console.debug("The logger supports many functions", "like appending arguments", join=", ")
    Console.warn("different logging levels with different colors")
    Console.error("and two loggers, for historical logging and session logging")
    Console.debug("You can also refer to an objects instance to find the logging message in your code", obj=Console)
    Console.warn("Or you change the color of a message and use *markdowns* to _decorate_ your text", color=AnsiCodes.blue)
    Console.debug("[nmd]Of course you *can deactivate _____ the markdown___ formatting")
