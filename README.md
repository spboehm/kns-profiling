# KNS-Profiling

## What is KNS-Profiling?

This repository contains all necessary components to perform an automated lifecycle analysis with KNS platforms.
A KNs platform is a Kubernetes-compatible container orchestration platform, like MicroK8s from Canonical and K3s maintained by Rancher.

This software project allows to simulate the lifecycle of a Kubernetes-platform entirely by monitoring the resource and time consumption of typical steps in cluster a lifecycle (like start master, joining/draining nodes).

The experiment is conducted by predefined ansible playbooks, which are located under `ansible/playbooks/profiling-***.yaml`.
During the experiment, different tasks of the playbooks store events into a mongodb instance in order to measure the resource and time consumption.
So far, we support the platform Kubernetes, MicroK8s, and K3s.

## Tool Architecture

tbd.

## How to Deploy the Profiling Tool?

tbd.

## How to Analyze the Obtained Data?

tbd.
