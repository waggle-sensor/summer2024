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

## Collection
Most of this information is fairly easy to collect. Through a combination of Kubernetes and NVIDIA Jetson utilities, we can obtain logs of an individual node's total resource consumption and the resource consumption per Kubernetes job.

The only challenge here will be converting this data into the format that we determine.

## Transmission
The transmission of this data is mostly a one-way process. An individual node should transmit data to a central server for storage, display, and analysis. For this direction, we can define an API that has the following JSON format:

```json
{
    "metadata": {
        "time-sent": "time log was sent",
        "sender": {
            "ip": "sender ip address",
            "name": "sender name" 
        }
    },
    "logs": [
        {
            "time-captured": "time log was captured",
            "log": {
                "name": "name",
                "resource": "cpu, gpu, memory, battery, etc",
                "source": "cadvisor, tegra",
                "value": "log value"
            }
        }
    ]
}
```

However, we also want this to be a configurable process. For this, we need to transmit data from some controller to an individual node. We define this configuration API as follows:

```json
{
    "config": {
        "callback": {
            "ip": "ip",
            "port": "port"
        },
        "chron": "chron"
    },
    "filters": [
        {
            "type": "include, exclude, etc",
            "tag": "name, ",
            "value": "value"
        }
    ]
} 
```

## Storage

## Display

## Analysis