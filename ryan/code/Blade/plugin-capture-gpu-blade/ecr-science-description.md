# Science

The distributed sensor network of Sage nodes has gathered thousands of images and continues collecting images daily. While these images contain useful features and information, it is difficult to find specific details without looking through each image individually. With computer vision models becoming more accurate, faster, and less parameter-intensive, there is an opportunity to efficiently describe the information in these images directly at the edge. Modern models can not only quickly describe images in the cloud but also provide near-instantaneous descriptions as they are captured at the nodes.

The purpose of this project is to use the node camera sensor along with a CPU or NVIDIA GPU in order to make descriptions of each captured image. 

# AI@Edge
This plugin deploys Microsoft's Florence-2-base computer vision model onto the specified node. The model can perform inferencing from a camera stream. 

When the plugin captures an image, the image is run through the "generateDescription" function. Within this function, Florence-2 is run three times. Each time it is run, there is a different prompt. These prompts are set by the Microsoft engineers in order to provide distinct and specific annotations.The prompts that are utilized on this plugin are: "MORE_DETAILED_CAPTION", "CAPTION_TO_PHRASE_GROUNDING", and "DENSE_REGION_CAPTION". 

- "MORE_DETAILED_CAPTION" provides a descriptive paragraph for the given image. 
- "CAPTION_TO_PHRASE_GROUNDING" reads the components from the detailed caption and attempts to identify where those components are within the image. So, for example, if the detailed caption was: "There is smoke on the tree", the phrase grounding would identify "smoke" and "tree" within the image.
- "DENSE_REGION_CAPTION" takes the regions of the image and tries to identify the components. This is useful when the detailed caption misses small information. If the image is primarily of a car but in the background there is a person, the dense region caption prompt is more likely to identify the person than the detailed caption prompt is. 

Each time Florence-2 is run, the function "run_example" runs. This function takes in the prompt and image. It includes adjustable variables such as the number of maximum tokens the model is allowed to generate and how many possible outputs the model should consider. It also performs post-processing which cleans up the text.

The prompts "CAPTION_TO_PHRASE_GROUNDING" and "DENSE_REGION_CAPTION" both produce box coordinates along with the identified components. Since boxing is not currently utilized, the program removes the list of coordinates before sending the results back to the user. In addition, any duplicates within both prompt results are removed. 

All of these prompts are combined in order to give the most comprehensive information to the user. In the end, once the information is published, the description will produce: 

 "DESCRIPTION: &nbsp;'MORE_DETAILED_CAPTION' &nbsp; LABELS:&nbsp; 'DENSE_REGION_CAPTION', 'CAPTION_TO_PHRASE_GROUNDING'" 

# Arguments
```
'-stream': ID or name of a stream, e.g. top-camera
'-out-dir': Path to save images locally in %Y-%m-%dT%H:%M:%S%z.jpg format
'-cronjob': Time interval expressed in cronjob style
```


# Reference

Xiao, B., Wu, H., Xu, W., Dai, X., Hu, H., Lu, Y., Zeng, M., Liu, C., & Yuan, L. (2023). *Florence-2: Advancing a unified representation for a variety of vision tasks*. arXiv preprint arXiv:2311.06242. Available at: https://arxiv.org/abs/2311.06242
