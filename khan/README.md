# MCS ANL Blog (Summer 2024)

## Preface

Computer Vision (CV), a field of Artificial Intelligence (AI), allows computers to interpret visual data from various sources like images and videos.

It involves the acquisition, processing, analysis, and understanding of digital images to extract high-dimensional data from the real world, producing numerical or symbolic information for machine use.

In image analysis, computers interpret images as matrices of numbers representing pixel color or intensity. Techniques like image classification, object detection, and semantic segmentation are commonly used.

Video analytics extends this approach to analyze video footage over time, extracting valuable insights such as counting people or identifying specific objects.

Deep Learning, a subset of machine learning, plays a pivotal role in image and video analysis by utilizing neural networks to learn data patterns.

In the context of video and image analysis, deep learning algorithms are utilized for object detection and tracking, as well as action recognition.

Popular techniques include Convolutional Neural Networks (CNNs) and models like Mask R-CNN, YOLOv3, YOLOR, and YOLOv7.

These techniques empower AI/ML models to comprehend the content of images and videos, enabling the identification of objects and actions within visual data.

## June 3rd

- Attended orientation.
- Located cubicles and offices for the MCS division.

## June 4th

- Completed 24 TMS trainings.
- Obtained badge.

## June 5th

- Researched and successfully prototyped with LLaVa and pre-trained open CLIP.
- Obtained proxy card.

## June 6th

- Wrote blog.
- Researched types of architectures and models avalable for temporal analysis.

## Friday, June 7th

**Weekly Goal:** Summarize and propose project improvements, scope, and milestones.

The primary objective of this project is to utilize object recognition, a specific computer vision task, in conjunction with a Large Language Model (LLM) to aid users in finding relevant images to download. Image captioning can convey the details of events within an image and becomes more feasible with sufficient temporal data from videos.

Computer Vision tasks like image classification, instance segmentation, semantic segmentation, and object recognition are not applicable to the project's goal.

Regarding LLM, popular architectures such as transformers, RNNs, and Mamba have drawbacks, including non-determinism and unreliable memory. To address these issues, a Generalized Action Representation (GAR) could be a possible research avenue.

**Proposed Approach:**

- Develop an algorithm for video/image captioning at the edge.
- Utilize it to send alerts (via API) based on classification (e.g., tornado warnings, flock of birds migration).
- Enable text and video/image search queries from sorted alerts.
- Implement Client LLM/RAG for analysis on images.
- Provide highlights of historical data from alerts with a recommendation system.

## June 10th

- Meeting to discuss goals in video captioning and image analysis.

## June 11th

- Extended research on replacing `scenic` with `pllava`.

## June 12th

- Guided tour of the Aurora supercomputer and Rapid Prototyping Laboratory.
- Visited the library to better understand older references available for research.

## Friday, June 17th

Blog Goal: Define the technologies that will be used to achieve the proposed milestones.
