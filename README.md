# Submission 123: Replication Package
*Hypertesting of Programs: Theoretical Foundation and Automated Test Generation*

---

The binaries of the tools `hyperfuzz` and `hyperevo` implementing our approach are provided in the directory [`bin/`](/bin), together with their configuration files. We also provide in the [`lib/`](/lib) directory the binaries of `phosphor`, that can be used to instrument Java code. Nevertheless, to run the experiments for the third research question you need a full installation of `phosphor` (see the [Requirements](#requirements) section).

> Experiments have been tested on a **Linux** machine (based on Ubuntu `20.04.3` LTS with Linux `5.11.0-27` kernel)

## Datasets
The [`datasets/`](/datasets) directory contains the sample Java programs (source code and configuration file indicating security tags) used in the evaluation. In particular:
- the [`datasets/UnsecureOnlyDataset/`](/datasets/UnsecureOnlyDataset) directory contains the samples comprising only the vulnerable programs (used in the first research question)
- the [`datasets/FullDataset/`](/datasets/FullDataset) directory contains all samples, vulnerable and non-vulnerable programs (used in the second and the third research questions)
- the [`datasets/FullDataset-phosphor/`](/datasets/FullDataset) directory contains all samples, vulnerable and non-vulnerable programs, modified in order to run with `phosphor` (used in the third research question)

## Pre-computed results
The `submission-results.tar.xz` archive contains the (complete) results that are reported in the submitted paper.

## How to run the experiments

### Requirements
Apart from the Python dependencies specified in the [`scripts/requirements.txt`](/scripts/requirements.txt) file, to run the experiments you need:
- Python (tested on Python `3.8.10`)
- a Java Runtime Environment (tested on OpenJDK `16.0.1`)
- the `phosphor` binaries and a `phosphor`-instrumented JVM

Follow the `phosphor` official [readme](https://github.com/gmu-swe/phosphor) to install the tool and instrument a JVM. To avoid some `phosphor` issues, it is recommended to instrument a **Java 16** virtual machine.

> In the `lib/` directory we provide an archive containing an already instrumented JVM

To use the provided instrumented JVM, unpack the archive and copy the `jre-inst/` directory into the `phosphor` root installation folder. The archive is split in three parts (`jre-inst.tar.xz.part0`, `jre-inst.tar.xz.part1` and `jre-inst.tar.xz.part2`), before unpacking you have to reconstruct the archive.
```console
foo@bar:~ReplicationPackage/lib$ cat jre-inst.tar.xz.part* > jre-inst.tar.xz
```

### Pre-processing
To run the experiments for the third research question, you have to first instrument with `phosphor` the Java programs contained in the [`datasets/FullDataset-phosphor/`](/datasets/FullDataset) directory. We provide a Python script that compiles, packs and instruments Java programs. *We assume to run the script from the root of the repository*.
```console
foo@bar:~ReplicationPackage$ python3 scripts/phosphorCodeInstrumenter.py instrument <dataset> [<options>]
```
where `dataset` is the directory containing the Java source code to instrument (e.g., `dataset/FullDataset-phosphor`) and `options` can be:
-	`-controlTrack`, to enable taint tracking through control flow [*not stable*]
- `-withoutBranchNotTaken`,	to disable branch not taken analysis in control tracking

> In the pre-computed results we used the option `-withoutBranchNotTaken`

The script also provides a `clean` command to remove already instrumented samples.

### Running
We provide three Python scripts, one for each research question, that run the experiments and compute the metrics. All scripts provide a `run` command, to run the experiments; and a `clean` command, to remove log files and already computed results. Results will be saved into the `results/` directory. *We assume to run the scripts from the root of the repository*.

#### First research question
```console
foo@bar:~ReplicationPackage$ python3 scripts/runExperimentRQ1.py run <dataset> <attempts> <sampling>
```
where `dataset` is the directory containing the sample Java programs (source code) to run (e.g., `dataset/VulnerableOnlyDataset`); `attempts` is the number of attempts in each test; and `sampling` is the number of samples used for the correlation.
> In the pre-computed results we set `1000` attempts, with sampling equal to `100`

#### Second research question
```console
foo@bar:~ReplicationPackage$ python3 scripts/runExperimentRQ2.py run <dataset> <runs>
```
where `dataset` is the directory containing the sample Java programs (source code) to run (e.g., `dataset/FullDataset`); and `runs` is the number of test repetitions.
> In the pre-computed results we performed `5` runs

#### Third research question
```console
foo@bar:~ReplicationPackage$ python3 scripts/runExperimentRQ3.py run <datasetHyper> <datasetPhosphor> <phosphorDir> <runs>
```
where `datasetHyper` is the directory containing the sample Java programs (source code) to run with `hyperfuzz` and `hyperevo` (e.g., `dataset/FullDataset`); `datasetPhosphor` is the directory containing the sample Java programs (instrumented `.jar` files) to run with `phosphor` (e.g., `dataset/FullDataset-phosphor`); `phosphorDir` is the directory where `phosphor` and the instrumented JVM are installed; and `runs` is the number of test repetitions.
> In the pre-computed results we performed `5` runs
