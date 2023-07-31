import sys
import os
import json

RUN_SCRIPT_NAME = "runExperimentRQ2"
SCRIPT_NAME = "computeMetricsRQ2"
FUZZING_STRATEGY = "hyperfuzz"
EVO_STRATEGY = "hyperevo"
PLOT_COLS = 5

def getResultFilesFromLogs():
    with open("scripts/{0}-{1}.log".format(RUN_SCRIPT_NAME, FUZZING_STRATEGY), "r") as file:
        line = file.readlines()[-1]
        logFuzz = line.split("\'")[1]
    with open("scripts/{0}-{1}.log".format(RUN_SCRIPT_NAME, EVO_STRATEGY), "r") as file:
        line = file.readlines()[-1]
        logEvo = line.split("\'")[1]
    return logFuzz, logEvo

def computeMetrics(resultsFile):
    resultsFileAbs = os.path.abspath(resultsFile)
    reportJson = json.load(open(resultsFileAbs))
    testRuns = reportJson["testRuns"]
    metrics = {}
    metrics["dataset"] = reportJson["dataset"]
    metrics["timestamp"] = reportJson["timestamp"]
    metrics["testRuns"] = testRuns
    samples = []
    for sample in reportJson["samples"]:
        metricsInfo = {}
        metricsInfo["sampleName"] = sample["sampleName"]
        metricsInfo["classFile"] = sample["classFile"]
        metricsInfo["methodName"] = sample["methodName"]
        metricsInfo["groundTruth"] = sample["groundTruth"]
        metricsInfo["totalGoals"] = sample["totalGoals"]
        metricsInfo["coverage"] = sample["coverage"]
        samples.append(metricsInfo)
    metrics["samples"] = samples
    return metrics

def combineMetrics(metricsFuzz, metricsEvo):
    metrics = {}
    metrics["dataset"] = metricsFuzz["dataset"]
    metrics["timestamp"] = metricsFuzz["timestamp"]
    metrics["testRuns"] = metricsFuzz["testRuns"]
    samples = []
    for i in range(len(metricsFuzz["samples"])):
        metricsInfo = {}
        metricsInfo["sampleName"] = metricsFuzz["samples"][i]["sampleName"]
        metricsInfo["classFile"] = metricsFuzz["samples"][i]["classFile"]
        metricsInfo["methodName"] = metricsFuzz["samples"][i]["methodName"]
        metricsInfo["groundTruth"] = metricsFuzz["samples"][i]["groundTruth"]
        metricsInfo["totalGoals"] = metricsFuzz["samples"][i]["totalGoals"]
        coverage = {}
        coverage[FUZZING_STRATEGY] = metricsFuzz["samples"][i]["coverage"]
        coverage[EVO_STRATEGY] = metricsEvo["samples"][i]["coverage"]
        metricsInfo["coverage"] = coverage
        samples.append(metricsInfo)
    metrics["samples"] = samples
    return metrics

def retrieveCSVTable(metrics):
    table = []
    for sample in metrics["samples"]:
        sampleName = sample["sampleName"].split(os.path.sep)[-1]
        totalGoals = sample["totalGoals"]
        coverageFuzz = sample["coverage"][FUZZING_STRATEGY]
        coverageEvo = sample["coverage"][EVO_STRATEGY]
        row = "{0};{1};{2:.2f};{3:.2f}".format(sampleName, totalGoals, coverageFuzz, coverageEvo)
        table.append(row)
    tableSorted = []
    tableSorted.append("SampleName;TotalGoals;CoverageHyperFuzz;CoverageHyperEvo")
    table.sort()
    tableSorted.extend(table)
    return tableSorted

def main():
    resultsFileFuzz, resultsFileEvo = getResultFilesFromLogs()
    metricsFile = resultsFileFuzz.replace(FUZZING_STRATEGY + "_", "").replace("/" + FUZZING_STRATEGY + "-", "_").replace("results.", "metrics.")
    metricsFuzz = computeMetrics(resultsFileFuzz)
    metricsEvo = computeMetrics(resultsFileEvo)
    metricsFileAbs = os.path.abspath(metricsFile)
    metrics = combineMetrics(metricsFuzz, metricsEvo)
    csvTable = retrieveCSVTable(metrics)
    metrics["csvTable"] = csvTable
    with open(metricsFileAbs, 'w', encoding = 'utf-8') as file:
        json.dump(metrics, file, ensure_ascii = False, indent = 4)
    print("\nMetrics saved into the file '{0}'".format(metricsFileAbs))

def printUsage():
	print("\nUsage: {0}.py".format(SCRIPT_NAME))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print("The script takes no argument...")
        printUsage()
        sys.exit()
    if not os.path.isfile("scripts/{0}-{1}.log".format(RUN_SCRIPT_NAME, FUZZING_STRATEGY)) or not os.path.isfile("scripts/{0}-{1}.log".format(RUN_SCRIPT_NAME, EVO_STRATEGY)):
        print("Error: no test log file(s) found. Execute 'scripts/{0}.py' script!".format(RUN_SCRIPT_NAME))
        sys.exit()
    main()
    sys.exit()
