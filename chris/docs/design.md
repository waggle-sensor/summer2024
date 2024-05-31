# System Design Document

## Problem Description
The SAGE/Waggle stack has no notion of resource consumption. This information is generally useful for

- Managing remote sensors that are battery powered
- Running intensive jobs
- Scheduling jobs based on resource utilization
- Increasing hardware longevity

However, without any notion of resource consumption, we are left guessing at how to best implement these. For example, the current scheduler is scheduled based on time and takes a conservative approach to resource management. This is best seen in how it manages GPU usage. Only one job that requires a GPU is allowed to run at a time. This conservative approach prevents GPU overload, but doesn't properly manage the entirety of the GPU's resources.

To begin working on the above problems, we want a wholistic and customizable way to gauge the resource utilization within the SAGE/Waggle stack. 

## Overview 
We can break down this problem into a few main parts:

- Collecting resource consumption info at the sensor level
- Transmitting this information
- Storing this information
- Displaying this information
- Analyzing this information

By keeping the main steps of this agnostic from the Waggle stack, we are able to create a generic library that can be used for all sorts of performance monitoring.

## Collection
Most of this information is fairly easy to collect. Through a combination of Kubernetes and NVIDIA Jetson utilities, we can obtain logs of an individual node's total resource consumption and the resource consumption per Kubernetes job.

The only challenge here is to convert metrics into the form that we want.

We also want to have the ability to collect more metrics in the future. To do this, we should set up some easy format to ingest metrics into Grafana.

## Transmission
Transmission is also fairly easy. By using the Grafana agent, we are able to use whatever infrastructure is defined for our storage. This can either be local Granfana storage or the Waggle infrastructure. All that is required here is to set up the Grafana agent.

## Storage
We want to create a fairly generic storage system. To make this project generic, we want to be able to plug and play with various types of storage.

### Local Storage
To approach using local storage, we want to be able to store Grafana metrics locally. One easy way to go about this is to us Mimir for local storage. This would allow us to view Grafana metrics locally. 

### Remote Storage for Waggle
The Waggle stack currently supports the use of Grafana metrics. This means that we only need to use the Grafana agent to push our metrics to the proper endpoint. There is currently Waggle code that handles this.

### Remote Storage in General
Going forward, we want to make it possible to use any Grafana endpoint for metrics storage and display. This should not be much more difficult than generalizing the remote storage for the Waggle stack.

## Display
We can use the Grafana display! 

## Analysis
Ultimately, we want to work towards building a system model from these metrics. More info to come.
