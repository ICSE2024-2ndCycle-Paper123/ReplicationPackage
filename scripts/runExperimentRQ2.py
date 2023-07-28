import os
import sys
import glob
import json
import shutil
from datetime import datetime
from statistics import mean
import computeMetricsRQ2

SCRIPT_NAME = "runExperimentRQ2"
THRESHOLD = 0.55
FUZZING_STRATEGY = "hyperfuzz"
EVO_STRATEGY = "hyperevo"
RESULTS_DIR = "RQ2"

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

def decodeResult(resultStr):
	if resultStr == "Unsafe method": 
		return 0
	if resultStr == "Likely safe method":
		return 1
	if resultStr == "Given up":
		return 2
	return -1

def getReportFileAbsolutePath(resultsDir, sampleDir, testStrategy, run):
	sampleName = os.path.normpath(sampleDir).split(os.path.sep)[-1]
	return "{0}/{1}/{2}_{3}-report_run{4}.json".format(os.path.abspath(resultsDir), sampleName, sampleName, testStrategy, run)

def getExecutionCommand(classFile, methodName, methodModifier, configFile, reportFile, testStrategy):
	if (methodModifier == "static"):
		cmd = "java -DlogFilename=bin/{0} -jar bin/{1}.jar -c={2} -m={3} --static -s={4} -r={5} -p=bin/{6}-config.conf >/dev/null 2>&1".format(testStrategy, testStrategy, classFile, methodName, configFile, reportFile, testStrategy)
	else:
		cmd = "java -DlogFilename=bin/{0} -jar bin/{1}.jar -c={2} -m={3} -s={4} -r={5} -p=bin/{6}-config.conf >/dev/null 2>&1".format(testStrategy, testStrategy, classFile, methodName, configFile, reportFile, testStrategy)
	return cmd

def getGroundTruth(sampleDir):
	sampleName = os.path.normpath(sampleDir).split(os.path.sep)[-1]
	if "unsecure" in sampleName:
		return 0
	else:
		return 1

def computeGlobalResult(resultList):
	unsafeCount = 0
	likelysafeCount = 0
	for result in resultList:
		if result == 0:
			unsafeCount += 1
		if result == 1:
			likelysafeCount += 1
	if unsafeCount > likelysafeCount and unsafeCount >= (THRESHOLD * len(resultList)):
		return 0
	if likelysafeCount > unsafeCount and likelysafeCount >= (THRESHOLD * len(resultList)):
		return 1
	return 2

def computeGlobalCoverage(coverageList):
	return mean(coverageList)

def run(testStrategy, datasetDir, testRuns):
	logFile = open("scripts/{0}-{1}.log".format(SCRIPT_NAME, testStrategy), "a")
	now = datetime.now()
	timestamp = now.strftime("%d-%m-%Y_%H%M%S")
	logFile.write("\n[{0}] Start testing classes in '{1}' folder\n".format(timestamp, os.path.abspath(datasetDir)))
	if not os.path.isdir("results"):
		os.mkdir("results")
	if not os.path.isdir("results/" + RESULTS_DIR):
		os.mkdir("results/" + RESULTS_DIR)
	resultsDir = "results/{0}/{1}_{2}".format(RESULTS_DIR, testStrategy, str(timestamp))
	os.mkdir(resultsDir)
	reportsDir = resultsDir + "/reports"
	os.mkdir(reportsDir)
	resultsReport = {}
	resultsReport["dataset"] = datasetDir
	resultsReport["timestamp"] = timestamp
	resultsReport["strategy"] = testStrategy
	resultsReport["testRuns"] = testRuns
	tests = []
	for sampleDir in glob.glob(datasetDir + "/*/"):
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
		resultList = []
		coverageList = []
		efficiencyFunctionList = []
		isError = True
		totalGoals = 0
		for i in range(testRuns):
			reportFile = getReportFileAbsolutePath(reportsDir, sampleDir, testStrategy, i)
			cmd = getExecutionCommand(classFile, methodName, methodModifier, configFile, reportFile, testStrategy)
			os.system(cmd)
			result = -1
			coverage = 0
			if os.path.isfile(reportFile):
				reportJson = json.load(open(reportFile))
				result = decodeResult(reportJson["analysisResult"])
				coverage = reportJson["coverage"]
				efficiencyFunction = reportJson["efficiencyFunction"]["functionValues"]
				totalGoals = reportJson["totalGoals"]
			if result != -1:
				isError = False
			resultList.append(result)
			coverageList.append(coverage)
			efficiencyFunctionList.append(efficiencyFunction)
		if isError:
			globalResult = -1
			globalCoverage = 0
			print("  Something went wrong during testing...")
			logFile.write("  {0} {1} -1\n".format(classFile, resultList))
		else:
			globalResult = computeGlobalResult(resultList)
			globalCoverage = computeGlobalCoverage(coverageList)
			if globalResult == 0:
				print("  Testing completed (coverage {0}): unsafe method --> {1}".format(globalCoverage, resultList))
			elif globalResult == 1:
				print("  Testing completed (coverage {0}): likely safe method --> {1}".format(globalCoverage, resultList))
			else:
				print("  Testing completed (coverage {0}): given up on the method --> {1}".format(globalCoverage, resultList))
			logFile.write("  {0} {1} {2}\n".format(classFile, resultList, globalResult))
		test["result"] = globalResult
		test["coverage"] = globalCoverage
		test["efficiencyFunctionList"] = efficiencyFunctionList
		test["totalGoals"] = totalGoals
		tests.append(test)
	resultsReport["samples"] = tests
	resultsReportFile = "{0}/{1}-results.json".format(resultsDir, testStrategy)
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
	if os.path.isfile("bin/{0}.log".format(EVO_STRATEGY)):
		os.unlink("bin/{0}.log".format(EVO_STRATEGY))
	if os.path.isfile("bin/{0}.log".format(FUZZING_STRATEGY)):
		os.unlink("bin/{0}.log".format(FUZZING_STRATEGY))
	if os.path.isfile("scripts/{0}-{1}.log".format(SCRIPT_NAME, FUZZING_STRATEGY)):
		os.unlink("scripts/{0}-{1}.log".format(SCRIPT_NAME, FUZZING_STRATEGY))
	if os.path.isfile("scripts/{0}-{1}.log".format(SCRIPT_NAME, EVO_STRATEGY)):
		os.unlink("scripts/{0}-{1}.log".format(SCRIPT_NAME, EVO_STRATEGY))

def printUsage():
	print("\nUsage: {0}.py <command> [<command_args>]".format(SCRIPT_NAME))
	print("  <command> can be either:")
	print("   'clean', to clean previous test result files, or")
	print("   'run', to run test executions\n")
	print("Command 'clean' takes no argument\n")
	print("Command 'run' takes the arguments list 'command_args': <dataset> <runs>")
	print("  <dataset> is the directory of the samples to test")
	print("  <runs> is the number of test repetitions\n")

if __name__ == "__main__":
	if len(sys.argv) == 2 and sys.argv[1] == "clean":
		clean()
		sys.exit()
	if len(sys.argv) == 4 and sys.argv[1] == "run":
		datasetDir = sys.argv[2]
		testRuns = int(sys.argv[3])
		if not os.path.isdir(datasetDir):
			print("Error: '{0}' is not a directory".format(datasetDir))
			sys.exit()
		if testRuns <= 0 or testRuns > 10:
			print("Warning: test repetitions out of bounds (setted to 1)")
			testRuns = 1
		print("\nStart test session: {0}".format(FUZZING_STRATEGY))
		run(FUZZING_STRATEGY, datasetDir, testRuns)
		print("\nEnd test session: {0}".format(FUZZING_STRATEGY))
		print("\nStart test session: {0}".format(EVO_STRATEGY))
		run(EVO_STRATEGY, datasetDir, testRuns)
		print("\nEnd test session: {0}".format(EVO_STRATEGY))
		print("\nComputing metrics...")
		computeMetricsRQ2.main()
		sys.exit()
	printUsage()
	sys.exit()