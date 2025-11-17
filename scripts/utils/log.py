# Log coloring (v1.3.0)

class Log:
    RESET = "\033[0m"
    COLORS = {
        "INFO": "\033[34m",
        "DRY":  "\033[33m",
        "OK":   "\033[32m",
        "ERROR":"\033[31m",
    }

    @staticmethod
    def _log(level, msg):
        color = Log.COLORS.get(level, "")
        print(f"{color}[{level}]{Log.RESET} {msg}")

    @staticmethod
    def info(msg):  Log._log("INFO", msg)
    @staticmethod
    def dry(msg):   Log._log("DRY", msg)
    @staticmethod
    def ok(msg):    Log._log("OK", msg)
    @staticmethod
    def error(msg): Log._log("ERROR", msg)
