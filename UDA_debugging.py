UDA_Debug = False

def debug_print(*args):
    if(globals()["UDA_Debug"]):
        for arg in args:
            print(arg, end="")
        print()

def set_debugging(val):
    globals()["UDA_Debug"] = val
    print("UDA_Debug: ", "ON" if val else "OFF")
