# KNS-Profiling

## What is KNS-Profiling?

This repository contains all necessary components to perform an automated lifecycle analysis with KNS platforms.
A KNs platform is a Kubernetes-compatible container orchestration platform, like MicroK8s from Canonical and K3s maintained by Rancher.

This software project allows to simulate the lifecycle of a Kubernetes-platform entirely by monitoring the resource and time consumption of typical steps in cluster a lifecycle (like start master, joining/draining nodes).

The experiment is conducted by predefined ansible playbooks, which are located under `ansible/simulate-***.yaml`.
During the experiment, different tasks that the playbook is referring to store events into a mongodb instance in order to measure the resource and time consumption.
So far, we support the platforms Kubernetes, MicroK8s, and K3s.

The following figure visualizes how the implementation is working:

![experimental-procedure](docs/img/experimental-setup-design-simulation-procedure.png "Experimental Procedure")

The experiment can be parametrized as follows. 

```yaml
  vars: 
    platform: "K3s"
    K3S_VERSION: v1.20.0+k3s2
    SIMULATION_WAIT_INTERVAL: "30" # paused time between tasks
    SIMULATION_IDLE_INTERVAL: "300" # time taken for measuring the idle utilization 
    SIMULATION_END_INTERVAL: "1000" # additional time after the experiment has been completed 

```

Furthermore, we can define the number of runs for the simulation:

```yaml
- include_tasks: profiling-k3s.yaml
    with_sequence: start=3060 end=3069 stride=1
    loop_control:
    loop_var: simulation
```

This will repeat the experiment 10 times.
The raw data of the experiment can be derived from a publicly available mongodb instance (read-only) with the following credentials:

```bash
user = guest
password = guest
host = h11.pi.uni-bamberg.de
port = 27017
ssl = true # only connections via ssh are allowed
```

We recommend R as tool for data analysis and provide a pre-configured r script which connects to the database and enables basic retrieval functions:

```r
# r-code/src/db.R
source("r-code/src/db.R")

# example simulation
simulation <- get.simulation(5000)

# involved hosts
hosts <- get.hosts(simulation$"_id")

# events during the simulation
events <- get.events.by.hosts.oid(5000, hosts$"_id"[1])

# metrics 
metrics <- get.system.metrics(5000, hosts$hostname, events$timestamp[1], events$timestamp[2])
```

The results of this r script are described here: tbd

## Tool Architecture

![experimental-setup-design](docs/img/experimental-setup-design.png "Experimental Setup")

## How to Deploy the Profiling Tool?

tbd.

## How to Analyze the Obtained Data?

tbd.