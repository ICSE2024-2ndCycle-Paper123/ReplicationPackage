import os
import sys
import glob
import json
import shutil
from datetime import datetime
from statistics import mean
import phosphorRun
import computeMetricsRQ3

SCRIPT_NAME = "runExperimentRQ3"
INSTRUMENTATION_SCRIPT_NAME = "phosphorCodeInstrumenter"
THRESHOLD = 0.55
FUZZING_STRATEGY = "hyperfuzz"
EVO_STRATEGY = "hyperevo"
RESULTS_DIR = "RQ3"
PHOSPHOR_NAME = "phosphor"
JAVAAGENT_BIN = "phosphor-jigsaw-javaagent-0.1.0-SNAPSHOT.jar"

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

def decodeResultHyperTest(resultStr):
	if resultStr == "Unsafe method": 
		return 0
	if resultStr == "Likely safe method":
		return 1
	if resultStr == "Given up":
		return 2
	return -1

def getTaintLabels(list):
    list = list.replace("[", "")
    list = list.replace("]", "")
    labels = []
    for label in list.split(","):
        label = label.strip()
        if "_" in label:
            labels.append(label.replace("_", ""))
        else:
            labels.append(label)
    return labels

def decodeResultPhosphor(resultArray, policy):
    taintedList = []
    index = 0
    for result in resultArray:
        if "is tainted" in result:
            taintedList.append(resultArray[index+1])
        index += 1
    taintedH = False
    if len(taintedList) > 0:
        for taintedRow in taintedList:
            labels = getTaintLabels(taintedRow.split(" ")[3])
        for label in labels:
            if label in policy:
                if policy[label] == "H":
                    taintedH = True
    if taintedH:
        return 0
    else:
        return 1

def getReportFileHyperTest(resultsDir, sampleDir, testStrategy, run):
	sampleName = os.path.normpath(sampleDir).split(os.path.sep)[-1]
	return "{0}/{1}/{2}_{3}-report_run{4}.json".format(os.path.abspath(resultsDir), sampleName, sampleName, testStrategy, run)

def getReportFilePhosphor(datasetDir):
    reportFile = glob.glob(datasetDir + "/*.json")[0]
    return reportFile

def getExecutionCommandHyperTest(classFile, methodName, methodModifier, configFile, reportFile, testStrategy):
	if (methodModifier == "static"):
		cmd = "java -DlogFilename=bin/{0} -jar bin/{1}.jar -c={2} -m={3} --static -s={4} -r={5} -p=bin/{6}-config.conf >/dev/null 2>&1".format(testStrategy, testStrategy, classFile, methodName, configFile, reportFile, testStrategy)
	else:
		cmd = "java -DlogFilename=bin/{0} -jar bin/{1}.jar -c={2} -m={3} -s={4} -r={5} -p=bin/{6}-config.conf >/dev/null 2>&1".format(testStrategy, testStrategy, classFile, methodName, configFile, reportFile, testStrategy)
	return cmd

def getExecutionCommandPhosphor(sampleDir, phosphorDir, jarFileAbsPath, className):
    phosphorDirAbsPath = os.path.abspath(phosphorDir)
    cmd = "cd {0}; jre-inst/bin/java -javaagent:phosphor-jigsaw-javaagent/target/{1} -cp {3} {4} > {2}/output.txt".format(phosphorDirAbsPath, JAVAAGENT_BIN, sampleDir, jarFileAbsPath, className)
    return cmd

def getGroundTruth(sampleDir):
	sampleName = os.path.normpath(sampleDir).split(os.path.sep)[-1]
	if "unsecure" in sampleName:
		return 0
	else:
		return 1

def computeGlobalResultHyperTest(resultList):
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

def computeGlobalResultPhosphor(resultList):
    return computeGlobalResultHyperTest(resultList)

def computeGlobalCoverage(coverageList):
	return mean(coverageList)

def getClassname(sampleDir):
    classFilePath = glob.glob(sampleDir + "/*.java")[0]
    classFile = os.path.normpath(classFilePath).split(os.path.sep)[-1]
    className = classFile.split(".")[0]
    return className

def runHyperTest(testStrategy, datasetDir, runs):
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
    resultsReport["testRuns"] = runs
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
        isError = True
        totalGoals = 0
        for i in range(runs):
            reportFile = getReportFileHyperTest(reportsDir, sampleDir, testStrategy, i)
            cmd = getExecutionCommandHyperTest(classFile, methodName, methodModifier, configFile, reportFile, testStrategy)
            os.system(cmd)
            result = -1
            coverage = 0
            if os.path.isfile(reportFile):
                reportJson = json.load(open(reportFile))
                result = decodeResultHyperTest(reportJson["analysisResult"])
                coverage = reportJson["coverage"]
                totalGoals = reportJson["totalGoals"]
            if result != -1:
                isError = False
            resultList.append(result)
            coverageList.append(coverage)
        if isError:
            globalResult = -1
            globalCoverage = 0
            print("  Something went wrong during testing...")
            logFile.write("  {0} {1} -1\n".format(classFile, resultList))
        else:
            globalResult = computeGlobalResultHyperTest(resultList)
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

def retrievePolicy(datasetDir, sampleName):
    for dir in glob.glob(datasetDir + "/*/"):
        if sampleName in dir:
            sampleDir = dir
    settingsFile = os.path.abspath(sampleDir) + "/settings.conf"
    policy = {}
    with open(settingsFile, 'r') as file:
        for line in file.readlines():
            key = line.split(":")[0].strip()
            value = line.split(":")[1].strip()
            if "@ArrayIndex" in value:
                value = value.split("@")[0].strip()
            policy[key] = value
    return policy

def runTaintAnalysis(datasetDir, phosphorDir, runs):
    logFile = open("scripts/{0}-{1}.log".format(SCRIPT_NAME, PHOSPHOR_NAME), "a")
    now = datetime.now()
    timestamp = now.strftime("%d-%m-%Y_%H%M%S")
    logFile.write("\n[{0}] Start analysing classes in '{1}' folder\n".format(timestamp, os.path.abspath(datasetDir)))
    if not os.path.isdir("results"):
        os.mkdir("results")
    if not os.path.isdir("results/" + RESULTS_DIR):
        os.mkdir("results/" + RESULTS_DIR)
    resultsDir = "results/{0}/{1}_{2}".format(RESULTS_DIR, PHOSPHOR_NAME, str(timestamp))
    os.mkdir(resultsDir)
    reportsDir = resultsDir + "/reports"
    os.mkdir(reportsDir)
    resultsReport = {}
    resultsReport["dataset"] = datasetDir
    resultsReport["timestamp"] = timestamp
    resultsReport["strategy"] = PHOSPHOR_NAME
    resultsReport["analysisRuns"] = runs
    allResults = []
    for i in range(runs):
        phosphorRun.main(datasetDir, phosphorDir, True)
        reportFilePath = getReportFilePhosphor(datasetDir)
        reportFile = os.path.normpath(reportFilePath).split(os.path.sep)[-1].split(".")[0]
        newReportFilePath = "{0}/{1}_run{2}.json".format(reportsDir, reportFile, i)
        cmd = "mv {0} {1}".format(reportFilePath, newReportFilePath)
        os.system(cmd)
        reportJson = json.load(open(newReportFilePath))
        samplesResult = []
        for sample in reportJson["samples"]:
            samplesResult.append((sample["sampleName"],sample["output"]))
        numSamples = len(samplesResult)
        allResults.append(samplesResult)
    analyses = []
    for i in range(numSamples):
        sampleName = allResults[0][i][0]
        sampleResults = []
        for j in range(runs):
            policy = retrievePolicy(datasetDir, sampleName)
            sampleResults.append(decodeResultPhosphor(allResults[j][i][1], policy))
        analysis = {}
        analysis["sampleName"] = sampleName
        if "unsecure" in sampleName:
            analysis["groundTruth"] = 0
        else:
            analysis["groundTruth"] = 1
        analysis["result"] = computeGlobalResultPhosphor(sampleResults)
        analyses.append(analysis)
    resultsReport["samples"] = analyses 
    resultsReportFile = "{0}/{1}-results.json".format(resultsDir, PHOSPHOR_NAME)
    with open(resultsReportFile, 'w', encoding = 'utf-8') as file:
        json.dump(resultsReport, file, ensure_ascii = False, indent = 4)
    now = datetime.now()
    timestamp = now.strftime("%d-%m-%Y_%H%M%S")
    logFile.write("[{0}] Ended analysing classes in '{1}' folder\n".format(timestamp, os.path.abspath(datasetDir)))
    logFile.write(" --> Results saved in '{0}' report file\n".format(resultsReportFile))
    logFile.close()

def areJarFilesPresent(datasetDir):
    arePresent = True
    for sampleDir in glob.glob(datasetDir + "/*/"):
        jarFiles = glob.glob(sampleDir + "/*.jar")
        if len(jarFiles) == 0:
            arePresent = False
    return arePresent

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
    if os.path.isfile("scripts/{0}-{1}.log".format(SCRIPT_NAME, PHOSPHOR_NAME)):
        os.unlink("scripts/{0}-{1}.log".format(SCRIPT_NAME, PHOSPHOR_NAME))

def printUsage():
    print("\nUsage: {0}.py <command> [<command_args>]".format(SCRIPT_NAME))
    print("  <command> can be either:")
    print("   'clean', to clean previous test result files, or")
    print("   'run', to run test executions\n")
    print("Command 'clean' takes no argument\n")
    print("Command 'run' takes the arguments list 'command_args': <datasetHypertest> <datasetPhosphor> <phosphorDir> <runs>")
    print("  <datasetHypertest> is the directory of the samples to test")
    print("  <datasetPhosphor> is the directory of the samples to test adapted to Phosphor")
    print("  <phosphorDir> is the directory where Phosphor and the instrumented JVM are installed")
    print("  <runs> is the number of test repetitions\n")

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "clean":
        clean()
        sys.exit()
    if len(sys.argv) == 6 and sys.argv[1] == "run":
        datasetDirHyperTest = sys.argv[2]
        datasetDirPhosphor = sys.argv[3]
        phosphorDir = sys.argv[4]
        runs = int(sys.argv[5])
        if not os.path.isdir(datasetDirHyperTest):
            print("Error: '{0}' is not a directory".format(datasetDirHyperTest))
            sys.exit()
        if not os.path.isdir(datasetDirPhosphor):
            print("Error: '{0}' is not a directory".format(datasetDirPhosphor))
            sys.exit()
        if runs <= 0 or runs > 10:
            print("Warning: test repetitions out of bounds (setted to 1)")
            runs = 1
        if not areJarFilesPresent(datasetDirPhosphor):
            print("Error: '{0}' does not contain instrumented code for all samples. Execute 'scripts/{1}.py' script!".format(datasetDirPhosphor, INSTRUMENTATION_SCRIPT_NAME))
            sys.exit()
        print("\nStart HyperTest session: {0}".format(FUZZING_STRATEGY))
        runHyperTest(FUZZING_STRATEGY, datasetDirHyperTest, runs)
        print("\nEnd HyperTest session: {0}".format(FUZZING_STRATEGY))
        print("\nStart HyperTest session: {0}".format(EVO_STRATEGY))
        runHyperTest(EVO_STRATEGY, datasetDirHyperTest, runs)
        print("\nEnd HyperTest session: {0}".format(EVO_STRATEGY))
        print("\nStart Taint Analysis session: {0}".format(PHOSPHOR_NAME))
        print("\n  Analyzing samples in '{0}'".format(datasetDirPhosphor))
        runTaintAnalysis(datasetDirPhosphor, phosphorDir, runs)
        print("\nEnd Taint Analysis session: {0}".format(PHOSPHOR_NAME))
        print("\nComputing metrics...")
        computeMetricsRQ3.main()
        sys.exit()
    printUsage()
    sys.exit()