# June 3rd, 2024

Began learning PyTorch and AI fundamentals

# June 4th, 2024

Started on Microsoft PyTorch training courses and started reading papers regarding image sparsification

# June 5th, 2024

Finished Microsoft training course and made notes on image sparsification papers. Began reading about OpenClip

# June 6th, 2024

Played around with OpenClip and wrote most of a paper in LaTeX about it. Tried to do image -> text and text -> image

# June 7th, 2024

Finished paper, had a meeting, and looked at ImageBind. Realized I need computing power and will begin to use the ANL computing resources available. 

# June 10th, 2024

Was onboarded with the HPC systems. Still need to learn how to work them. Also tried to work out how to get OpenCLIP to figure out what is inside an image

# June 11th, 2024

CLIP does not pay attention to specific details within an image, only the image as a whole. This means there has to be a way to classify little components. First, I tried to split all of the images into 16 block segments. Sadly, this means it cuts some of the critical peices and confuses OpenCLIP. I decided that I need to do feature segmentation. That first led me to "GroupViT" but after a lot of trying, their code is just broken and big. I am now trying to use MS COCO with PyTorch--maybe OpenCLIP would help too. What would be great is to use OpenCLIP but force it to do feature segmentation by looking really hard. OC is really lazy and thinks clouds are trucks with 90% certianty so I'm not sure what to do with that. Also when I put in "there is a small little unicorn in this picture" it returned 3 SAGE images. I didn't see any unicorns.  
