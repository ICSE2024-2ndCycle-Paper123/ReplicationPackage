import os
import sys
import glob
import json
import shutil
from datetime import datetime
import computeMetricsRQ1

SCRIPT_NAME = "runExperimentRQ1"
RESULTS_DIR = "RQ1"

def getClassName(sampleDir):
	classFiles = glob.glob(sampleDir + "/program/*.java")
	className, _ = os.path.splitext(os.path.basename(classFiles[0]))
	return className

def getMethodName(sampleDir):
	with open(sampleDir + "/method.txt", "r") as file:
		methodName = file.readlines()[0]
		return methodName.strip()

def getMethodModifier(sampleDir):
	with open(sampleDir + "/method.txt", "r") as file:
		methodModifier = file.readlines()[1]
		return methodModifier.strip()

def getReportFileAbsolutePath(resultsDir, sampleDir):
	sampleName = os.path.normpath(sampleDir).split(os.path.sep)[-1]
	return "{0}/{1}/{2}_hypercoveragetester-report.json".format(os.path.abspath(resultsDir), sampleName, sampleName)

def getExecutionCommand(classFile, methodName, methodModifier, configFile, reportFile, attempts, samplingSize):
	if (methodModifier == "static"):
		cmd = "java -DlogFilename=bin/hypercoveragetester -jar bin/hypercoveragetester.jar -c={0} -m={1} --static -s={2} -r={3} -p={4} -z={5} >/dev/null 2>&1".format(classFile, methodName, configFile, reportFile, attempts, samplingSize)
	else:
		cmd = "java -DlogFilename=bin/hypercoveragetester -jar bin/hypercoveragetester.jar -c={0} -m={1} -s={2} -r={3} -p={4} -z={5} >/dev/null 2>&1".format(classFile, methodName, configFile, reportFile, attempts, samplingSize)
	return cmd

def getGroundTruth(sampleDir):
	sampleName = os.path.normpath(sampleDir).split(os.path.sep)[-1]
	if "unsecure" in sampleName:
		return "unsecure"
	else:
		return "secure"

def computeCoverageViolationsFunction(numberOfElements, coveredGoalsList, violationsList):
	coverageViolationsFunction = []
	for i in range(numberOfElements):
		coverageViolationsFunction.append((coveredGoalsList[i], violationsList[i]))
	return coverageViolationsFunction

def run(datasetDir, attempts, sampling):
	logFile = open("{0}.log".format("scripts/" + SCRIPT_NAME), "a")
	now = datetime.now()
	timestamp = now.strftime("%d-%m-%Y_%H%M%S")
	logFile.write("\n[{0}] Start testing classes in '{1}' folder\n".format(timestamp, os.path.abspath(datasetDir)))
	if not os.path.isdir("results"):
		os.mkdir("results")
	if not os.path.isdir("results/" + RESULTS_DIR):
		os.mkdir("results/" + RESULTS_DIR)
	resultsDir = "results/{0}/hypercoveragetester_{1}".format(RESULTS_DIR, str(timestamp))
	os.mkdir(resultsDir)
	reportsDir = resultsDir + "/reports"
	os.mkdir(reportsDir)
	resultsReport = {}
	resultsReport["dataset"] = datasetDir
	resultsReport["timestamp"] = timestamp
	resultsReport["attempts"] = attempts
	resultsReport["sampling"] = sampling
	tests = []
	for sampleDir in glob.glob(datasetDir+"/*/"):
		os.mkdir(reportsDir + "/" + os.path.normpath(sampleDir).split(os.path.sep)[-1])
		sampleDirAbs = os.path.abspath(sampleDir)
		classFile = glob.glob(sampleDirAbs + "/program/*.java")[0]
		methodName = getMethodName(sampleDirAbs)
		methodModifier = getMethodModifier(sampleDirAbs)
		configFile = sampleDirAbs + "/settings.conf"
		print("\nTesting '{0}'".format(sampleDirAbs))
		test = {}
		test["sampleName"] = sampleDir[sampleDir.index("/")+1:-1]
		test["classFile"] = classFile
		test["methodName"] = methodName
		test["groundTruth"] = getGroundTruth(sampleDir)
		reportFile = getReportFileAbsolutePath(reportsDir, sampleDir)
		cmd = getExecutionCommand(classFile, methodName, methodModifier, configFile, reportFile, attempts, sampling) 
		os.system(cmd)
		result = "Error"
		if os.path.isfile(reportFile):
			reportJson = json.load(open(reportFile))
			goals = reportJson["goals"]
			violations = reportJson["violations"]
			coverageStatsJson = reportJson["coverageStats"]
			result = reportJson["result"]
			test["goals"] = goals
			test["violations"] = violations
			coverageStats = {}
			coverageStats["numberOfElements"] = coverageStatsJson["numberOfElements"]
			coverageStats["goals"] = coverageStatsJson["allGoals"]
			coverageStats["violations"] = coverageStatsJson["allViolations"]
			coverageStats["coverageViolationsFunction"] = computeCoverageViolationsFunction(coverageStatsJson["numberOfElements"], coverageStatsJson["coveredGoalsList"], coverageStatsJson["violationsList"])	
			test["coverageStats"] = coverageStats	
		if result == "Error":
			print("  Something went wrong during testing...")
			logFile.write("  {0} Error\n".format(classFile))
		else:
			print("  Testing completed succesfully...")
			logFile.write("  {0} Ok\n".format(classFile))
			tests.append(test)
	resultsReport["samples"] = tests
	resultsReportFile = "{0}/hypercoveragetester-results.json".format(resultsDir)
	with open(resultsReportFile, 'w', encoding = 'utf-8') as file:
		json.dump(resultsReport, file, ensure_ascii = False, indent = 4)
	now = datetime.now()
	timestamp = now.strftime("%d-%m-%Y_%H%M%S")
	logFile.write("[{0}] Ended testing classes in '{1}' folder\n".format(timestamp, os.path.abspath(datasetDir)))
	logFile.write(" --> Results saved in '{0}' report file\n".format(resultsReportFile))
	logFile.close()

def clean():
	if os.path.isdir("results/" + RESULTS_DIR):
		for root, dirs, files in os.walk("results/" + RESULTS_DIR):
			for f in files:
				os.unlink(os.path.join(root, f))
			for d in dirs:
				shutil.rmtree(os.path.join(root, d))
		os.rmdir("results/" + RESULTS_DIR)
	if os.path.isfile("bin/hypercoveragetester.log"):
		os.unlink("bin/hypercoveragetester.log")
	if os.path.isfile("scripts/{0}.log".format(SCRIPT_NAME)):
		os.unlink("scripts/{0}.log".format(SCRIPT_NAME))

def printUsage():
	print("\nUsage: {0}.py <command> [<command_args>]".format(SCRIPT_NAME))
	print("  <command> can be either:")
	print("   'clean', to clean previous test result files, or")
	print("   'run', to run test executions\n")
	print("Command 'clean' takes no argument\n")
	print("Command 'run' takes the arguments list 'command_args': <dataset> <attempts> <sampling>")
	print("  <dataset> is the directory of the samples to test")
	print("  <attempts> is the number of attempts in a test")
	print("  <sampling> is the number of samples used for the correlation\n")

if __name__ == "__main__":
	if len(sys.argv) == 2 and sys.argv[1] == "clean":
		clean()
		sys.exit()
	if len(sys.argv) == 5 and sys.argv[1] == "run":
		datasetDir = sys.argv[2]
		attempts = int(sys.argv[3])
		sampling = int(sys.argv[4])
		if not os.path.isdir(datasetDir):
			print("Error: '{0}' is not a directory".format(datasetDir))
			sys.exit()
		if attempts <= 0 or attempts > 10000:
			print("Warning: attempts out of bounds (setted to 100)")
			attempts = 100
		if sampling <= 0 or sampling > (attempts / 10):
			print("Warning: incorrect sampling (setted to {0})".format(attempts / 10))
			sampling = attempts / 10
		print("\nStart test session")
		run(datasetDir, attempts, sampling)
		print("\nEnd test session")
		print("\nComputing metrics...")
		computeMetricsRQ1.main()
		sys.exit()
	printUsage()
	sys.exit()