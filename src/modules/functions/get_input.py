def get_input(inps, args):
    for a in args:
        if a in inps:
            return args[a]
    print("Error getting: {}".format(inps))
    return None