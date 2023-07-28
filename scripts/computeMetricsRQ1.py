import sys
import os
import warnings
import json
import numpy as np
import scipy.stats as sps
import matplotlib.pyplot as pplt
import math

PVALUE = 0.05
RUN_SCRIPT_NAME = "runExperimentRQ1"
SCRIPT_NAME = "computeMetricsRQ1"
PLOT_COLS = 4

def computePearson(xVector, yVector):
    pearsonJson = {}
    X = np.array(xVector)
    Y = np.array(yVector)
    pearson_r, pearson_pvalue = sps.pearsonr(X, Y)
    if math.isnan(pearson_r):
        pearsonJson["r"] = "_"
    else:
        pearsonJson["r"] = pearson_r
    if math.isnan(pearson_pvalue):
        pearsonJson["p-value"] = "_"
    else:
        pearsonJson["p-value"] = pearson_pvalue
    return pearsonJson, (pearson_r, pearson_pvalue)

def computeSpearman(xVector, yVector):
    spearmanJson = {}
    X = np.array(xVector)
    Y = np.array(yVector)
    spearman_rho, spearman_pvalue = sps.spearmanr(X, Y)
    if math.isnan(spearman_rho):
        spearmanJson["rho"] = "_"
    else:
        spearmanJson["rho"] = spearman_rho
    if math.isnan(spearman_pvalue):
        spearmanJson["p-value"] = "_"
    else:
        spearmanJson["p-value"] = spearman_pvalue
    return spearmanJson, (spearman_rho, spearman_pvalue)

def computeKendall(xVector, yVector):
    kendallJson = {}
    X = np.array(xVector)
    Y = np.array(yVector)
    kendall_tau, kendall_pvalue = sps.kendalltau(X, Y)
    if math.isnan(kendall_tau):
        kendallJson["tau"] = "_"
    else:
        kendallJson["tau"] = kendall_tau
    if math.isnan(kendall_pvalue):
        kendallJson["p-value"] = -1
    else:
        kendallJson["p-value"] = kendall_pvalue
    return kendallJson, (kendall_tau, kendall_pvalue)

def computePointBiserial(xVector, binVector):
    pointbiserialJson = {}
    BIN = np.array(binVector)
    X = np.array(xVector)
    pointbiserial_R, pointbiserial_pvalue = sps.pointbiserialr(BIN, X)
    if math.isnan(pointbiserial_R):
        pointbiserialJson["R"] = "_"
    else:
        pointbiserialJson["R"] = pointbiserial_R
    if math.isnan(pointbiserial_pvalue):
        pointbiserialJson["p-value"] = -1
    else:
        pointbiserialJson["p-value"] = pointbiserial_pvalue
    return pointbiserialJson, (pointbiserial_R, pointbiserial_pvalue)

def binaryzeViolations(yVector):
    binVector = []
    for i in range(len(yVector)):
        if yVector[i] > 0:
            binVector.append(True)
        else:
            binVector.append(False)
    return binVector

def printPvalue(pvalue):
    if pvalue < PVALUE:
        return "{0:.3f} < {1:.2f}".format(pvalue, PVALUE)
    else:
        return "{0:.2f} <= {1:.3f}".format(PVALUE, pvalue)

def getResultFileFromLog():
    with open("scripts/{0}.log".format(RUN_SCRIPT_NAME), "r") as file:
        line = file.readlines()[-1]
        return line.split("\'")[1]

def computeMetrics(resultsFile):
    resultsFileAbs = os.path.abspath(resultsFile)
    reportJson = json.load(open(resultsFileAbs))
    metrics = {}
    metrics["dataset"] = reportJson["dataset"]
    metrics["timestamp"] = reportJson["timestamp"]
    metrics["attempts"] = reportJson["attempts"]
    metrics["sampling"] = reportJson["sampling"]
    samples = []
    for sample in reportJson["samples"]:
        metricsInfo = {}
        metricsInfo["sampleName"] = sample["sampleName"]
        metricsInfo["classFile"] = sample["classFile"]
        metricsInfo["methodName"] = sample["methodName"]
        metricsInfo["groundTruth"] = sample["groundTruth"]
        metricsInfo["goals"] = sample["goals"]
        metricsInfo["violations"] = sample["violations"]
        xVector = []
        yVector = []
        for functionEntry in sample["coverageStats"]["coverageViolationsFunction"]:
            xVector.append(functionEntry[0])
            yVector.append(functionEntry[1])
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
        pearsonJson, _ = computePearson(xVector, yVector)
        spearmanJson, _ = computeSpearman(xVector, yVector)
        kendallJson, _ = computeKendall(xVector, yVector)
        binVector = binaryzeViolations(yVector)
        pointbiserialJson, _ = computePointBiserial(xVector, binVector)
        metricsInfo["pearson"] = pearsonJson
        metricsInfo["spearman"] = spearmanJson
        metricsInfo["kendall"] = kendallJson
        metricsInfo["pointbiserial"] = pointbiserialJson
        metricsInfo["coverageViolationsFunction"] = sample["coverageStats"]["coverageViolationsFunction"]
        samples.append(metricsInfo)
    metrics["samples"] = samples
    return metrics

def plotMetrics(plotsFile, metrics):
    numPlots = len(metrics["samples"])
    rows = math.ceil(numPlots / PLOT_COLS)
    fig, axs = pplt.subplots(rows, PLOT_COLS, figsize=(PLOT_COLS * 4, rows * 4))
    listIndex = 0
    for i in range(rows):
        if i == rows - 1 and numPlots - listIndex < PLOT_COLS:
            cols = numPlots - listIndex
        else:
            cols = PLOT_COLS
        for j in range(cols):
            sample = metrics["samples"][listIndex]
            sampleName = sample["sampleName"].split(os.path.sep)[-1]
            coverageViolationsFunction = sample["coverageViolationsFunction"]
            xVector = []
            yVector = []
            for functionEntry in coverageViolationsFunction:
                xVector.append(functionEntry[0])
                yVector.append(functionEntry[1])
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
            _, pearson = computePearson(xVector, yVector)
            _, spearman = computeSpearman(xVector, yVector)
            _, kendall = computeKendall(xVector, yVector)
            binVector = binaryzeViolations(yVector)
            _, pointbiserial = computePointBiserial(xVector, binVector)
            X = np.array(xVector)
            Y = np.array(yVector)
            pearsonLine = "Pearson: {0:.3f} ({1})".format(pearson[0], printPvalue(pearson[1]))
            spearmanLine = "Spearman: {0:.3f} ({1})".format(spearman[0], printPvalue(spearman[1]))
            kendallLine = "Kendall: {0:.3f} ({1})".format(kendall[0], printPvalue(kendall[1]))
            pointbiserialLine = "PointBiserial: {0:.3f} ({1})".format(pointbiserial[0], printPvalue(pointbiserial[1]))
            slope, intercept, _, _, _ = sps.linregress(X, Y)
            if rows == 1:
                axs[j].plot(X, Y, linewidth = 0, marker = '.', label = "Data points")
                axs[j].plot(X, intercept + slope * X, label = "Regression line")
                axs[j].set_xlabel("Coverage")
                axs[j].set_ylabel("Violations")
                axs[j].legend(facecolor = 'white')
                caption = sampleName + "\n" + pearsonLine + "\n" + spearmanLine + "\n" + kendallLine + "\n" + pointbiserialLine
                axs[j].set_title(caption)
            else:
                axs[i, j].plot(X, Y, linewidth = 0, marker = '.', label = "Data points")
                axs[i, j].plot(X, intercept + slope * X, label = "Regression line")
                axs[i, j].set_xlabel("Coverage")
                axs[i, j].set_ylabel("Violations")
                axs[i, j].legend(facecolor = 'white')
                caption = sampleName + "\n" + pearsonLine + "\n" + spearmanLine + "\n" + kendallLine + "\n" + pointbiserialLine
                axs[i, j].set_title(caption)
            listIndex += 1
    fig.tight_layout()
    pplt.savefig(plotsFile, bbox_inches = 'tight')

def retrieveCSVTable(metrics):
    table = []
    for sample in metrics["samples"]:
        sampleName = sample["sampleName"].split(os.path.sep)[-1]
        pointbiserial = sample["pointbiserial"]
        if pointbiserial["R"] == "_":
            RStr = "_"
        else:
            RStr = "{0:.4f}".format(float(pointbiserial["R"]))
        if pointbiserial["p-value"] == "_" or pointbiserial["p-value"] == -1:
            pValueStr = "_"
        else:
            pValueStr = "{0:.4f}".format(float(pointbiserial["p-value"]))
        row = "{0};{1};{2}".format(sampleName, RStr, pValueStr)
        table.append(row)
    tableSorted = []
    tableSorted.append("SampleName;R;p-value")
    table.sort()
    tableSorted.extend(table)
    return tableSorted

def main():
    resultsFile = getResultFileFromLog()
    metrics = computeMetrics(resultsFile)
    metricsFile = resultsFile.replace("results.", "metrics.")
    plotsFile = os.path.abspath(str(metricsFile).replace("metrics.json", "plots.pdf"))
    plotMetrics(plotsFile, metrics)
    csvTable = retrieveCSVTable(metrics)
    metrics["csvTable"] = csvTable
    metricsFileAbs = os.path.abspath(metricsFile)
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
    if not os.path.isfile("scripts/{0}.log".format(RUN_SCRIPT_NAME)):
        print("Error: no test log file found. Execute 'scripts/{0}.py' script!".format(RUN_SCRIPT_NAME))
        sys.exit()
    main()
    sys.exit()

