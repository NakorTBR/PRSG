class debug_colours:


    '''Colors class:reset all colours with debug_colours.reset; two
    sub classes fg for foreground
    and bg for background; use as debug_colours.subclass.colourname.
    i.e. debug_colours.fg.red or debug_colours.bg.green to use.  
    Also, the generic bold, disable, underline, reverse, strike through,
    and invisible work with the main class i.e. debug_colours.bold'''
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'

    class fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'

    class bg:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'

    # print(debug_colours.bg.green, "SKk", debug_colours.fg.red, "Amartya")
    # print(debug_colours.bg.lightgrey, "SKk", debug_colours.fg.red, "Amartya")
