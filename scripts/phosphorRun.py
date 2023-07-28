import sys
import os
import glob
import json
from datetime import datetime

SCRIPT_NAME = "phosphorRun"
PHOSPHOR_BIN = "Phosphor-0.1.0-SNAPSHOT.jar"
JAVAAGENT_BIN = "phosphor-jigsaw-javaagent-0.1.0-SNAPSHOT.jar"

def getRunCommand(sampleDir, phosphorDir, jarFile, className):
    absSampleDir = os.path.abspath(sampleDir)
    absPhosphorDir = os.path.abspath(phosphorDir)
    cmd = "cd {0}; jre-inst/bin/java -javaagent:phosphor-jigsaw-javaagent/target/{1} -cp {2}/{3} {4} > {2}/output.txt".format(absPhosphorDir, JAVAAGENT_BIN, absSampleDir, jarFile, className)
    return cmd

def getOutputContent(sampleDir):
    absSampleDir = os.path.abspath(sampleDir)
    outputFile = absSampleDir + "/output.txt"
    output = []
    with open(outputFile, 'r') as file:
        for line in file.readlines():
            if "Phosphor" in line:
                output.append(line.strip())
    os.remove(outputFile)
    return output

def main(datasetDir, phosphorDir, silent):
    now = datetime.now()
    timestamp = now.strftime("%d-%m-%Y_%H%M%S")
    report = {}
    report["dataset"] = datasetDir
    report["timestamp"] = timestamp
    samples = []
    for sampleDir in glob.glob(datasetDir + "/*/"):
        jarFilePath = glob.glob(sampleDir + "/*.jar")[0]
        jarFile = os.path.normpath(jarFilePath).split(os.path.sep)[-1]
        if not silent:
            print("\nRunning sample '{0}{1}'".format(sampleDir, jarFilePath))
        sample = {}
        sample["sampleName"] = sampleDir[sampleDir.index("/")+1:-1]
        classFilePath = glob.glob(sampleDir + "/*.java")[0]
        classFile = os.path.normpath(classFilePath).split(os.path.sep)[-1]
        className = classFile.split(".")[0]
        runCommand = getRunCommand(sampleDir, phosphorDir, jarFile, className)
        os.system(runCommand)
        output = getOutputContent(sampleDir)
        sample["output"] = output
        samples.append(sample)
    report["samples"] = samples
    reportFile = "{0}/{1}-report_{2}.json".format(os.path.abspath(datasetDir), SCRIPT_NAME.replace(".py", ""), timestamp)
    with open(reportFile, 'w', encoding = 'utf-8') as file:
        json.dump(report, file, ensure_ascii = False, indent = 4)
    if not silent:
        print("\nResults saved into the file '{0}'".format(reportFile))

def printUsage():
    print("\nUsage: {0}.py [-silent] <dataset> <phosphorDir>".format(SCRIPT_NAME))
    print("  -silent is a flag that suppresses stdout messages")
    print("  <dataset> is the directory of the samples instrumented binaries")
    print("  <phosphorDir> is the directory where Phosphor and the instrumented JVM are installed")

if __name__ == "__main__":
    if len(sys.argv) == 3 or (len(sys.argv) == 4 and sys.argv[1] == "-silent"):
        if (len(sys.argv) == 4):
            silent = True
            datasetDir = sys.argv[2]
            phosphorDir = sys.argv[3]
        else:
            silent = False
            datasetDir = sys.argv[1]
            phosphorDir = sys.argv[2]
        if not os.path.isdir(datasetDir):
            print("Error: '{0}' is not a directory".format(datasetDir))
            sys.exit()
        if not os.path.isdir(phosphorDir):
            print("Error: '{0}' is not a directory".format(phosphorDir))
            sys.exit()
        main(datasetDir, phosphorDir, silent)
        sys.exit()
    printUsage()
    sys.exit()