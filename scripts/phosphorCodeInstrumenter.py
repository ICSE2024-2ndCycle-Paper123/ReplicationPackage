import sys
import os
import glob

SCRIPT_NAME = "phosphorCodeInstrumenter"
PHOSPHOR_BIN = "Phosphor-0.1.0-SNAPSHOT.jar"
BASE_OPTIONS_STR = "" #"-withoutBranchNotTaken"

'''
 Phosphor option:
	-controlTrack,				Enable taint tracking through control flow (not stable)
	-withoutBranchNotTaken,		Disable branch not taken analysis in control tracking
'''

def getCopyCommand(sampleDir):
	absSampleDir = os.path.abspath(sampleDir)
	cmd = "cp lib/{0} {1}".format(PHOSPHOR_BIN, absSampleDir)
	return cmd

def getCompileCommand(sampleDir, classFile):
	absSampleDir = os.path.abspath(sampleDir)
	cmd = "cd {0}; javac -cp {1} {2}".format(absSampleDir, PHOSPHOR_BIN, classFile)
	return cmd

def createManifestFile(sampleDir, classFile):
	className = classFile.split(".")[0]
	manifestConent = "Manifest-Version: 1.0\n"
	manifestConent = manifestConent + "Main-Class: {0}\n".format(className)
	manifestConent = manifestConent + "Class-Path: {0}\n\n".format(PHOSPHOR_BIN)
	manifestFilePath = os.path.abspath(sampleDir) + "/manifest.txt"
	with open(manifestFilePath, 'w') as file:
		file.write(manifestConent)

def getPackingCommand(sampleDir, classFile):
	absSampleDir = os.path.abspath(sampleDir)
	jarName = "{0}.jar".format(classFile.split(".")[0])
	cmd = "cd {0}; jar cvfm {1} manifest.txt *.class >/dev/null 2>&1".format(absSampleDir, jarName)
	return cmd

def getPhosphorOptionsString(options):
	optionsStr = BASE_OPTIONS_STR
	if len(options) > 0:
		for option in options:
			optionsStr = optionsStr + " " + option
	return optionsStr

def getInstrumentationCommand(sampleDir, classFile, options):
	absSampleDir = os.path.abspath(sampleDir)
	className = classFile.split(".")[0]
	optionsStr = getPhosphorOptionsString(options)
	logFile = "scripts/" + SCRIPT_NAME + ".log"
	with open(logFile, 'a') as file:
		file.write("\nInstrumenting file '{0}{1}'\n".format(sampleDir, classFile))
	cmd = "java -jar lib/{0} {3} {1}/{2}.jar {1}/instrumented >> {4} 2>&1".format(PHOSPHOR_BIN, absSampleDir, className, optionsStr, logFile)
	return cmd

def getCleanupCommand(sampleDir, classFile):
	absSampleDir = os.path.abspath(sampleDir)
	className = classFile.split(".")[0]
	mvcmd = "mv {0}/instrumented/{1}.jar {0}/{1}-instrumented.jar".format(absSampleDir, className)
	rmcmd = "rm {0}/*.class; rm -R {0}/instrumented; rm {0}/{1}.jar; rm {0}/{2}; rm {0}/manifest.txt".format(absSampleDir, className, PHOSPHOR_BIN)
	if os.path.isdir("debug-preinst") :
		rmcmd = rmcmd + "; rm -R debug-preinst"
	if os.path.isfile("lastClass.txt"):
		rmcmd = rmcmd + "; rm lastClass.txt"
	return mvcmd + "; " + rmcmd

def main(datasetDir, options):
	for sampleDir in glob.glob(datasetDir + "/*/"):
		print(sampleDir)
		classFilePath = glob.glob(sampleDir + "/*.java")[0]
		classFile = os.path.normpath(classFilePath).split(os.path.sep)[-1]
		print("\nInstrumenting sample '{0}{1}'".format(sampleDir, classFile))
		copycmd = getCopyCommand(sampleDir)
		os.system(copycmd)
		compilecmd = getCompileCommand(sampleDir, classFile)
		os.system(compilecmd)
		createManifestFile(sampleDir, classFile)
		packingCommand = getPackingCommand(sampleDir, classFile)
		os.system(packingCommand)
		instrumentationCommand = getInstrumentationCommand(sampleDir, classFile, options)
		os.system(instrumentationCommand)
		cleanupCommand = getCleanupCommand(sampleDir, classFile)
		os.system(cleanupCommand)
		logFile = "scripts/" + SCRIPT_NAME + ".log"
	with open(logFile, 'a') as file:
		file.write("\nInstrumentation of '{0}' completed".format(os.path.abspath(datasetDir)))
	print("\nInstrumentation completed")

def parseOptions(sysArgv):
	options = []
	if len(sysArgv) == 4:
		options.append(sysArgv[3])
	if len(sysArgv) == 5:
		options.append(sysArgv[3])
		options.append(sysArgv[4])
	return options

def clean():
	logFile = "scripts/" + SCRIPT_NAME + ".log"
	if os.path.isfile(logFile):
		with open(logFile, 'r') as file:
			line = file.readlines()[-1]
		datasetDir = line.split("'")[1]
		for sampleDir in glob.glob(datasetDir + "/*/"):
			jarFile = glob.glob(sampleDir + "/*.jar")[0]
			os.unlink(jarFile)
		os.unlink(logFile)

def printUsage():
	print("\nUsage: {0}.py <command> [<command_args>]".format(SCRIPT_NAME))
	print("  <command> can be either:")
	print("   'clean', to clean previously instrumented files, or")
	print("   'instrument', to run instrumentation\n")
	print("Command 'clean' takes no argument\n")
	print("Command 'instrument' takes the arguments list 'command_args': <dataset> <options>")
	print("  <dataset> is the directory of the samples source code to instrument")
	print("  <options> is the space-separate list of Phosphor options")
	print("\nSupported Phosphor options:")
	print("  -controlTrack, to enable taint tracking through control flow (not stable)")
	print("  -withoutBranchNotTaken, to disable branch not taken analysis in control tracking")

if __name__ == "__main__":
	if len(sys.argv) == 2 and sys.argv[1] == "clean":
		clean()
		sys.exit()
	if len(sys.argv) > 2 and len(sys.argv) <= 5 and sys.argv[1] == "instrument":
		datasetDir = sys.argv[2]
		if not os.path.isdir(datasetDir):
			print("Error: '{0}' is not a directory".format(datasetDir))
			sys.exit()
		if not os.path.isfile("lib/" + PHOSPHOR_BIN):
			print("Error: intrumenter 'lib/{0}' missing".format(PHOSPHOR_BIN))
			sys.exit()
		options = parseOptions(sys.argv)
		main(datasetDir, options)
		sys.exit()
	printUsage()
	sys.exit()
