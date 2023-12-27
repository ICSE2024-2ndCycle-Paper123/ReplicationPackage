# Artifact: Replication Package
Related to the paper:

> Pasqua Michele, Ceccato Mariano and Tonella Paolo. 2024. **Hypertesting of Programs: Theoretical Foundation and Automated Test Generation**. In: *Proceedings of the 46<sup>th</sup> IEEE/ACM International Conference on Software Engineering* (ICSE '24). ACM, 1-11. *(to appear)*.

## Purpose

The primary goal of the artifact is to facilitate the replication of the results reported in the empirical evaluation of the companion paper. Such evaluation empirically validates the novel hypercoverage criterion and hypertesting approach proposed in the paper, by considering a specific hyperproperty for security, *Non-Interference*. The empirical study is guided by three research questions:
- ***RQ<sub>1</sub> (Correlation)***, assessing if hypercoverage correlates with the exposure of hyperproperty violations;
- ***RQ<sub>2</sub> (Coverage)***, assessing if the proposed hypertest input generators can achieve high coverage; and
- ***RQ<sub>3</sub> (Effectiveness)***, assessing if the hypertest inputs generated under the guidance of hypercoverage can effectively expose hyperproperty violations.

The artifact makes also available a dataset of Java programs, together with ground-truth security tags, that can be used to assess the effectiveness of detection tools targeting Non-Interference violations. Finally, the artifact provides the executables and the usage documentation of the tools `hyperfuzz` and `hyperevo`, the two hypertest input generators presented in the companion paper.

## Content

The artifact is an archive containing the following files:
- the [`README.md`](/README.md) file, describing the artifact
- the [`LICENSE`](/LICENSE) file
- a copy [`ICSE24paper.pdf`](/ICSE24paper.pdf) of the pre-print version of the companion paper
- the `submission-results.tar.xz` file, containing the pre-computed results reported in the companion paper

and the following directories:
- [`bin/`](/bin), containing the executables of `hyperfuzz` and `hyperevo` (used in RQ<sub>2</sub> and RQ<sub>3</sub>), and the executable `hypercoveragetester.jar` (used in RQ<sub>1</sub>)
- [`datasets/`](/datasets), containing all datasets of Java programs used in the experiments
- [`lib/`](/lib), containing a pre-instrumented JVM and the executable of `phosphor` (used in RQ<sub>3</sub>)
- [`scripts/`](/scripts), containing all Python scripts used to run experiments and compute metrics

> The artifact also provides a Virtual Machine ([`HyperEvo-Artifact.ova`](/HyperEvo-Artifact.ova)), to replicate experiments in a clean environment with all dependencies installed. See the section [Virtual Environment](#virtual-environment) of this readme for details.

## Data

The sample programs used in the empirical evaluation consists in 34 vulnerable and non-vulnerable Java classes (source code) taken from the public dataset `IFSpec` [2]. The latter, is a collection of freely-usable Java applications that are by design vulnerable or non-vulnerable to Non-Interference.

In `IFSpec`, variables are already tagged with security levels, taken from a security lattice, by using *RIFL* specifications. In the evaluation, we simplified the security tagging of variables: for each sample class we manually provided a `settings.conf` file containing a simple mapping `var:secTag`, where `secTag` can be either `L`, indicating a *public* variable, or `H`, indicating a *confidential* variable. Samples name has been provided with a trailing string indicating the ground-truth: `secure`, meaning that the sample does not contain a Non-Interference vulnerability; or `unsecure`, meaning that the sample do contain a Non-Interference vulnerability.

To answer RQ<sub>1</sub> only the vulnerable programs are needed, consisting in 14 Java classes having a Non-Interference vulnerability. Finally, since `phosphor` requires a manual modification of the program source code, in order to insert the information needed to perform instrumentation, we also provide the modified versions of all 34 vulnerable and non-vulnerable samples.

The [`datasets/`](/datasets) directory contains the sample Java programs (source code and configuration file indicating security tags) used in the evaluation. In particular:
- the [`datasets/UnsecureOnlyDataset/`](/datasets/UnsecureOnlyDataset) directory contains the samples comprising only the vulnerable programs (used in RQ<sub>1</sub>)
- the [`datasets/FullDataset/`](/datasets/FullDataset) directory contains all samples, vulnerable and non-vulnerable programs (used in RQ<sub>2</sub> and RQ<sub>3</sub>)
- the [`datasets/FullDataset-phosphor/`](/datasets/FullDataset) directory contains all samples, vulnerable and non-vulnerable programs, modified in order to run with `phosphor` (used in RQ<sub>3</sub>)

> The [`submission-results.tar.xz`](/submission-results.tar.xz) archive contains the ***pre-computed results*** that are reported in the companion paper.

## Setup

To run the experiments no particular hardware is required. All experiments have been tested on a laptop having the following configuration:
- 11th Gen Intel Core i5-1135G7 CPU
- 8 GiB of RAM
- an integrated Intel Xe Graphics (TGL GT2)

> Experiments have been tested on a **Linux** machine (based on Ubuntu `20.04.3` LTS with Linux `5.11.0-27` kernel).

### Requirements
Apart from the Python dependencies specified in the [`scripts/requirements.txt`](/scripts/requirements.txt) file, that you can install by using `pip`,
```console
foo@bar:~ReplicationPackage$ pip install -r scripts/requirements.txt
```
to run the experiments you need:
- Python3 (tested on Python `3.8.10`)
- a Java Runtime Environment (tested on OpenJDK `16.0.1`)
- the `phosphor` binaries and a `phosphor`-instrumented JVM

You can follow the `phosphor` official [readme](https://github.com/gmu-swe/phosphor) to install the tool and instrument a JVM. To avoid some `phosphor` issues, it is recommended to instrument a **Java 16** virtual machine.

Alternatively, you can use the provided `phosphor` install script as described in the following. **[recommended]**

In the `lib/` directory we provide an archive containing an already instrumented JVM and the `phosphor` binaries. We also provide a Python script that installs both the JVM and the binaries. *We assume to run the script from the root directory of the unpacked artifact folder*.
```console
foo@bar:~ReplicationPackage$ python3 scripts/phosphorInstallFromLocal.py install <phosphorDir>
```
where `phosphorDir` is the directory where `phosphor` and the instrumented JVM will be installed.

## How to run the experiments

To easily run the experiments and collect the results, we provide some Python scripts. All scripts come with an ***usage*** and are described in the following.

### Pre-processing

To run the experiments for RQ<sub>3</sub>, you have to first instrument with `phosphor` the Java programs contained in the [`datasets/FullDataset-phosphor/`](/datasets/FullDataset) directory. We provide a Python script that compiles, packs and instruments Java programs. *We assume to run the script from the root directory of the unpacked artifact folder*.
```console
foo@bar:~ReplicationPackage$ python3 scripts/phosphorCodeInstrumenter.py instrument <dataset> [<options>]
```
where `dataset` is the directory containing the Java source code to instrument (e.g., `datasets/FullDataset-phosphor`) and `options` can be:
-	`-controlTrack`, to enable taint tracking through control flow **[not stable]**
- `-withoutBranchNotTaken`,	to disable branch not taken analysis in control tracking

> In the pre-computed results we used the option `-withoutBranchNotTaken`.

The script also provides a `clean` command to remove already instrumented samples.

### Running

We provide three Python scripts, one for each research question, that run the experiments and compute the metrics (and output results). All scripts provide a `run` command, to run the experiments; and a `clean` command, to remove log files and already computed results. Results will be saved into the `results/` directory. *We assume to run the script from the root directory of the unpacked artifact folder*.

#### RQ<sub>1</sub> (Correlation)

To run the experiment for the first research question, you can run:
```console
foo@bar:~ReplicationPackage$ python3 scripts/runExperimentRQ1.py run <dataset> <attempts> <sampling>
```
where `dataset` is the directory containing the sample Java programs (source code) to run (e.g., `datasets/VulnerableOnlyDataset`); `attempts` is the number of attempts in each test; and `sampling` is the number of samples used for the correlation.
> In the pre-computed results we set `1000` attempts, with sampling equal to `100`.

#### RQ<sub>2</sub> (Coverage)

To run the experiment for the second research question, you can run:
```console
foo@bar:~ReplicationPackage$ python3 scripts/runExperimentRQ2.py run <dataset> <runs>
```
where `dataset` is the directory containing the sample Java programs (source code) to run (e.g., `datasets/FullDataset`); and `runs` is the number of test repetitions.
> In the pre-computed results we performed `5` runs.

#### RQ<sub>3</sub> (Effectiveness)

To run the experiment for the third research question, you can run:
```console
foo@bar:~ReplicationPackage$ python3 scripts/runExperimentRQ3.py run <datasetHyper> <datasetPhosphor> <phosphorDir> <runs>
```
where `datasetHyper` is the directory containing the sample Java programs (source code) to run with `hyperfuzz` and `hyperevo` (e.g., `datasets/FullDataset`); `datasetPhosphor` is the directory containing the sample Java programs (instrumented `.jar` files) to run with `phosphor` (e.g., `datasets/FullDataset-phosphor`); `phosphorDir` is the directory where `phosphor` and the instrumented JVM are installed; and `runs` is the number of test repetitions.
> In the pre-computed results we performed `5` runs.

## Virtual Environment

We also provide a virtual machine containing all datasets, binaries and dependencies needed to replicate the experiments in a clean environment. The virtual environment is a fully operating system (based on Lubuntu `20.04.5`) distributed as a virtual image ([`HyperEvo-Artifact.ova`](/HyperEvo-Artifact.ova)) in the *Open Virtualization Format*.

To import and launch the virtual image you can use [VirtualBox](https://www.virtualbox.org/). Once the virtual system is up and running, you can use the same Python scripts described in the section [How to run the experiments](#how-to-run-the-experiments).

**[important]** In the virtual environment
- the ***root directory*** of the replication package (where to run the Python scripts) is: `/home/icse2024ae/ReplicationPackage`
- the `phosphor` ***installation directory*** is: `/home/icse2024ae/phosphor`

As an example, to run the experiment for RQ<sub>3</sub> you should open a terminal in the virtual system and type
```console
icse2024ae@icse2024ae-virtualbox:~$ cd ReplicationPackage/
```
to move in the replication package root directory. Then type
```console
icse2024ae@icse2024ae-virtualbox:~ReplicationPackage$ python3 scripts/phosphorCodeInstrumenter.py instrument datasets/FullDataset-phosphor -withoutBranchNotTaken
```
to instrument the Java programs with `phosphor`. And, finally, type
```console
icse2024ae@icse2024ae-virtualbox:~ReplicationPackage$ python3 scripts/runExperimentRQ3.py run datasets/FullDataset datasets/FullDataset-phosphor /home/icse2024ae/phosphor 5
```
to run the experiment and compute the results. The latter will be saved in the directory `/home/icse2024ae/ReplicationPackage/results/`.

## Test Generators Usage
