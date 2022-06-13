import _Object.object as object

def newError(*args):
    return object.Error(args[0].format(*args[1:]))