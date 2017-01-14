debugging = False

def debug_print(*args):
    if(globals()["debugging"]):
        for arg in args:
            print(arg, end="")
        print()

def set_debugging(val):
    globals()["debugging"] = val
    print("Debugging: ", "ON" if val else "OFF")
