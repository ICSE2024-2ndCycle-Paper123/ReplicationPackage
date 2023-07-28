import sys
import os
import json

RUN_SCRIPT_NAME = "runExperimentRQ3"
SCRIPT_NAME = "computeMetricsRQ3"
FUZZING_STRATEGY = "hyperfuzz"
EVO_STRATEGY = "hyperevo"
PHOSPHOR_NAME = "phosphor"
PLOT_COLS = 5

def getResultFilesFromLogs():
    with open("scripts/{0}-{1}.log".format(RUN_SCRIPT_NAME, FUZZING_STRATEGY), "r") as file:
        line = file.readlines()[-1]
        logFuzz = line.split("\'")[1]
    with open("scripts/{0}-{1}.log".format(RUN_SCRIPT_NAME, EVO_STRATEGY), "r") as file:
        line = file.readlines()[-1]
        logEvo = line.split("\'")[1]
    with open("scripts/{0}-{1}.log".format(RUN_SCRIPT_NAME, PHOSPHOR_NAME), "r") as file:
        line = file.readlines()[-1]
        logPhosphor = line.split("\'")[1]
    return logFuzz, logEvo, logPhosphor

def computeMetrics(resultsFile):
    resultsFileAbs = os.path.abspath(resultsFile)
    reportJson = json.load(open(resultsFileAbs))
    if "testRuns" in reportJson:
        runs = reportJson["testRuns"]
    else:
        runs = reportJson["analysisRuns"]
    metrics = {}
    metrics["dataset"] = reportJson["dataset"]
    metrics["timestamp"] = reportJson["timestamp"]
    metrics["runs"] = runs
    tp = 0
    fp = 0
    fn = 0
    tn = 0
    samples = []
    for sample in reportJson["samples"]:
        metricsInfo = {}
        metricsInfo["sampleName"] = sample["sampleName"]
        groundTruth = sample["groundTruth"]
        metricsInfo["groundTruth"] = groundTruth
        result = sample["result"]
        metricsInfo["result"] = result
        if groundTruth == 0 and result == 0:
            metricsInfo["category"] = "TP"
            tp += 1
        if groundTruth == 1 and result == 0:
            metricsInfo["category"] = "FP"
            fp += 1
        if groundTruth == 0 and (result == 1 or result == 2):
            metricsInfo["category"] = "FN"
            fn += 1
        if groundTruth == 1 and (result == 1 or result == 2):
            metricsInfo["category"] = "TN"
            tn += 1
        samples.append(metricsInfo)
    if fn + tp == 0:
        tpr = "_"
    else:
        tpr = tp / (fn + tp)
    if tn + fp == 0:
        fpr = "_"
    else:
        fpr = fp / (tn + fp)
    if tp + fn == 0:
        fnr = "_"
    else:
        fnr = fn / (tp + fn)
    if fn + fp + tp + tn == 0:
        acc = "_"
    else:
        acc = (tp + tn) / (fn + fp + tp + tn)
    metrics["TPR"] = tpr
    metrics["FPR"] = fpr
    metrics["FNR"] = fnr
    metrics["ACC"] = acc
    metrics["samples"] = samples
    return metrics


def combineMetrics(metricsFuzz, metricsEvo, metricsPhosphor):
    metrics = {}
    metrics["dataset"] = metricsFuzz["dataset"]
    metrics["timestamp"] = metricsFuzz["timestamp"]
    metrics["runs"] = metricsFuzz["runs"]
    tpr = {}
    tpr[FUZZING_STRATEGY] = metricsFuzz["TPR"]
    tpr[EVO_STRATEGY] = metricsEvo["TPR"]
    tpr[PHOSPHOR_NAME] = metricsPhosphor["TPR"]
    metrics["TPR"] = tpr
    fpr = {}
    fpr[FUZZING_STRATEGY] = metricsFuzz["FPR"]
    fpr[EVO_STRATEGY] = metricsEvo["FPR"]
    fpr[PHOSPHOR_NAME] = metricsPhosphor["FPR"]
    metrics["FPR"] = fpr
    fnr = {}
    fnr[FUZZING_STRATEGY] = metricsFuzz["FNR"]
    fnr[EVO_STRATEGY] = metricsEvo["FNR"]
    fnr[PHOSPHOR_NAME] = metricsPhosphor["FNR"]
    metrics["FNR"] = fnr
    acc = {}
    acc[FUZZING_STRATEGY] = metricsFuzz["ACC"]
    acc[EVO_STRATEGY] = metricsEvo["ACC"]
    acc[PHOSPHOR_NAME] = metricsPhosphor["ACC"]
    metrics["ACC"] = acc
    samples = []
    for i in range(len(metricsFuzz["samples"])):
        metricsInfo = {}
        metricsInfo["sampleName"] = metricsFuzz["samples"][i]["sampleName"]
        metricsInfo["groundTruth"] = metricsFuzz["samples"][i]["groundTruth"]
        result = {}
        result[FUZZING_STRATEGY] = (metricsFuzz["samples"][i]["result"], metricsFuzz["samples"][i]["category"])
        result[EVO_STRATEGY] = (metricsEvo["samples"][i]["result"], metricsEvo["samples"][i]["category"])
        result[PHOSPHOR_NAME] = (metricsPhosphor["samples"][i]["result"], metricsPhosphor["samples"][i]["category"])
        metricsInfo["result"] = result
        samples.append(metricsInfo)
    metrics["samples"] = samples
    return metrics

def printStringMetric(metric):
    if metric == "_" or metric == "nan":
        return "_"
    else:
        return "{0:.2f}".format(float(metric))

def printResult(result):
    if result == 0:
        return "unsecure"
    else:
        return "secure"
def retrieveCSVTable(metrics):
    tableSorted = []
    tableSorted.append("Metrics;Phosphor;HyperFuzz;HyperEvo")
    tpr = "TPR;{0};{1};{2}".format(printStringMetric(metrics["TPR"][PHOSPHOR_NAME]), printStringMetric(metrics["TPR"][FUZZING_STRATEGY]), printStringMetric(metrics["TPR"][EVO_STRATEGY]))
    tableSorted.append(tpr)
    fpr = "FPR;{0};{1};{2}".format(printStringMetric(metrics["FPR"][PHOSPHOR_NAME]), printStringMetric(metrics["FPR"][FUZZING_STRATEGY]), printStringMetric(metrics["FPR"][EVO_STRATEGY]))
    tableSorted.append(fpr)
    fnr = "FNR;{0};{1};{2}".format(printStringMetric(metrics["FNR"][PHOSPHOR_NAME]), printStringMetric(metrics["FNR"][FUZZING_STRATEGY]), printStringMetric(metrics["FNR"][EVO_STRATEGY]))
    tableSorted.append(fnr)
    acc = "ACC;{0};{1};{2}".format(printStringMetric(metrics["ACC"][PHOSPHOR_NAME]), printStringMetric(metrics["ACC"][FUZZING_STRATEGY]), printStringMetric(metrics["ACC"][EVO_STRATEGY]))
    tableSorted.append(acc)
    tableSorted.append("Sample;Ground Truth;Phosphor;HyperFuzz;HyperEvo")
    table = []
    for sample in metrics["samples"]:
        row = "{0};{1};{2};{3};{4}".format(sample["sampleName"], printResult(sample["groundTruth"]), printResult(sample["result"][PHOSPHOR_NAME][0]), printResult(sample["result"][FUZZING_STRATEGY][0]), printResult(sample["result"][EVO_STRATEGY][0]))
        table.append(row)
    table.sort()
    tableSorted.extend(table)
    return tableSorted

def main():
    resultsFileFuzz, resultsFileEvo, resultFilePhosphor = getResultFilesFromLogs()
    metricsFile = resultsFileFuzz.replace(FUZZING_STRATEGY + "_", "").replace("/" + FUZZING_STRATEGY + "-", "_").replace("results.", "metrics.")
    metricsFuzz = computeMetrics(resultsFileFuzz)
    metricsEvo = computeMetrics(resultsFileEvo)
    metricsPhosphor = computeMetrics(resultFilePhosphor)
    metricsFileAbs = os.path.abspath(metricsFile)
    metrics = combineMetrics(metricsFuzz, metricsEvo, metricsPhosphor)
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
    if not os.path.isfile("scripts/{0}-{1}.log".format(RUN_SCRIPT_NAME, FUZZING_STRATEGY)) or not os.path.isfile("scripts/{0}-{1}.log".format(RUN_SCRIPT_NAME, EVO_STRATEGY)) or not os.path.isfile("scripts/{0}-{1}.log".format(RUN_SCRIPT_NAME, PHOSPHOR_NAME)):
        print("Error: no testing/analysis log file(s) found. Execute 'scripts/{0}.py' script!".format(RUN_SCRIPT_NAME))
        sys.exit()
    main()
    sys.exit()