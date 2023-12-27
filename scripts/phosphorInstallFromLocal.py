import sys
import os

SCRIPT_NAME = "phosphorInstallFromLocal"
PHOSPHOR_BIN = "Phosphor-0.1.0-SNAPSHOT.jar"
JVM_TAR = "jre-inst.tar.xz"
JAVAAGENT_TAR = "phosphor-jigsaw-javaagent.tar.xz"

def getUnpackCommand(tarFile, targetDir):
    absTarFile = os.path.abspath(tarFile)
    absTargetDir = os.path.abspath(targetDir)
    cmd = "tar -xf {0} -C {1}".format(tarFile, targetDir)
    return cmd

def main(phosphorDir):
    print("\nCopying Phosphor binaries...")
    absPhosphorBinDir = os.path.abspath(phosphorDir + "/Phosphor/target/")
    os.makedirs(absPhosphorBinDir, exist_ok=True)
    copyCommand = "cp lib/{0} {1}".format(PHOSPHOR_BIN, absPhosphorBinDir)
    os.system(copyCommand)
    print("\nUnpacking instrumented JVM...")
    unpackJVMCommand = getUnpackCommand("lib/" + JVM_TAR, phosphorDir)
    os.system(unpackJVMCommand)
    print("\nUnpacking Java Agent...")
    unpackJavaAgentCommand = getUnpackCommand("lib/" + JAVAAGENT_TAR, phosphorDir)
    os.system(unpackJavaAgentCommand)
    print("\nPhosphor and instrumented JVM successfully installed in '{0}'".format(phosphorDir))

def printUsage():
    print("\nUsage: {0}.py install <phosphorDir>".format(SCRIPT_NAME))
    print("  <phosphorDir> is the directory where Phosphor and the instrumented JVM will be installed")

if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "install":
        phosphorDir = sys.argv[2]
        if not os.path.isdir(phosphorDir):
            print("Error: '{0}' is not a directory".format(phosphorDir))
            sys.exit()
        main(phosphorDir)
        sys.exit()
    printUsage()
    sys.exit()
