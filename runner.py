import re
import sys
import os
import importlib

import click


def runner():
    if len(sys.argv) != 3:
        click.echo("Not enough params. Expecting modules and arguments as parameters")

    modules = sys.argv[1].split(",")
    argDict = generateArgumentsDict(sys.argv[2])

    for module in modules:
        importModule = importlib.import_module("modules." + module)
        arg = {}
        if module in argDict:
            arg = argDict[module]
        importModule.run(arg)

    for oneoff in os.listdir(os.path.join(os.path.dirname(os.path.realpath(__file__)),'one')):
        if oneoff[-3:] == ".py":
            if oneoff[:-3] != "__init__":
                importModule = importlib.import_module("one." + oneoff[:-3])
                importModule.run()
                if oneoff[:-3] != "test":
                    oneoffFilePath = os.path.join(os.path.dirname(os.path.realpath(__file__)),'one',oneoff)
                    click.echo("Deleting " + oneoffFilePath)
                    os.remove(oneoffFilePath)

def generateArgumentsDict(arguments):
    argDict = {}
    # module1(name:josh,length:8);module2(name:josh)
    args = arguments.split(";")
    for arg in args:
        # module1(name:josh,length:8)
        moduleArgsDict = {}
        moduleName = arg[:arg.find("(")]
        moduleArgs = re.search('[\d\w]+\(([\d\w\,\:]+)\)', arg)
        if moduleArgs:
            splitModuleArgs = moduleArgs.group(1).split(",")
            for smArg in splitModuleArgs:
                splitSMArg = smArg.split(":")
                moduleArgsDict[splitSMArg[0]] = splitSMArg[1]
        argDict[moduleName] = moduleArgsDict
    return argDict

    


if __name__ == "__main__":
    runner()
