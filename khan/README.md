# MCS ANL Blog

## Preface

Computer Vision (CV), a subset of Artificial Intelligence (AI), enables computers to interpret visual data from images and videos by acquiring, processing, and analyzing digital images to extract meaningful information. Techniques such as image classification, instance segmentation, semantic segmentation, and object detection are widely used in CV. These tasks rely heavily on deep learning algorithms, such as Convolutional Neural Networks (CNNs), which are essential for effectively tracking objects and recognizing actions within visual data. CV empowers AI models, like Large Language Models (LLMs), to efficiently understand and identify objects and activities within visual data, thereby enhancing AI models' ability to comprehend and generate insights from multimedia content.

The objective of this project is to leverage the notion of object recognition, a particular CV task, in conjunction with an LLM to aid users in discovering, downloading, and asking about relevant images or videos. Dense captioning, especially when enriched with sufficient temporal data gleaned from videos, significantly enhances descriptive capabilities.

## Ideal Proposed Development Approach

- Develop or select an algorithm for image or video captioning at the edge.
- Use it to send alerts (via API) based on classification
    - Warnings (tornado, flood, accidents)
    - Information (flock of birds migrating, deer eating)
- Enable text (and image or video) search queries from sorted alerts.
- Implement client LLM or RAG for analysis on images.
    - Luminous objects (sun, reflection on solar panel)
    - Colors, number of cars and deformations on car
    - Predict next flock of birds using historical data
    - Why did they migrate (seasonal changes)
- Provide highlights of historical data from alerts with a recommendation system.
    - Cater to specific user intent with alerts recommendation system

## Weekly Goals

- Week 1: Propose and summarize project scope, improvements, and milestones.
- Week 2: Define the technologies that will be used to achieve the proposed milestones.
- Week 3: Conduct thorough research, selection, implementation, evaluation, presentation, and demonstration of papers.
- Week 4: Create framework to deploy the technologies and create a presentation on the selected model implementation.
- Week 5: Deploy the technologies and create poster.

## Further Research

Exploring improvements for LLMs, including [efficiency](https://arxiv.org/abs/2406.02528) and architectural considerations like Transformers, Recurrent Neural Networks (RNNs), and [Mamba](https://arxiv.org/abs/2406.07522), a Generalized Action Representation (GAR) broadly akin to [Husky](https://arxiv.org/abs/2406.06469) could notably enhance the utility of LLMs.

I primarily research using [Google Scholar](https://scholar.google.com) and [Papers With Code](https://paperswithcode.com).

## June 3rd (Week 1)

- Attended orientation, gaining insights into culture, policies, and procedures.
- Located cubicles and office space for the MCS division.

## June 4th

- Completed 24 TMS trainings.
- Obtained badge.

## June 5th

- Researched and successfully prototyped with pre-trained LLaVa, OpenCLIP, and ImageBind.
- Obtained proximity card to access fitness facility.

## June 6th

- Researched types of architectures and models avalable for temporal analysis.
- Wrote blog outlining the strategic approach on implementing state-of-the-art models.

## June 7th

- Fleshed out proposed development approach for long-term planning.
- Initiated detailed research on Google's [Scenic](https://github.com/google-research/scenic/tree/main/scenic/projects) dense captioning implementations.

## June 10th (Week 2)

- Continued research on Google's Scenic.
- Begun to experiment with other models.

## June 11th

- Met to discuss goals with dense captioning and image or video analysis.
- Extended research on replacing Google's Scenic with PLLaVA.

## June 12th

- Continued research on replacing Google's Scenic with PLLaVA.
- Guided tour of the Aurora supercomputer and Rapid Prototyping Laboratory.
- Visited the library to better understand older references available for research.

## June 13th

- Conducted tests with PLLaVA.
- Continued, commited, and pushed blog.

## June 14th

- Continued tests with PLLaVA.
- Continued, commited, and pushed blog.

## June 17th (Week 3)

- Reorganized scope, ideas, and planning.
- Initiate very detailed research from a broad scope.

## June 18th

- Continued, commited, and pushed blog.
- Continued very detailed research from a broad scope.

## June 19th

- Used dashboard as well as sage_data_client to test on both image and video data.
- Continued, commited, and pushed blog.
- Wrapped up research to create a presentation on selection, implementation, evaluation, presentation, and demonstration of papers.

## June 20th

- Present on selection, implementation, evaluation, presentation, and demonstration of papers.

## June 21st
