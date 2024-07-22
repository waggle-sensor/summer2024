import torch
from config import *
from PIL import Image
from utils.utils import *
import torch.nn.functional as F
from trol.load_trol import load_trol
from torchvision.transforms.functional import pil_to_tensor

def main():
    link = "TroL-1.8B"
    prompt_type = "with_image"
    img_path = './sample.jpg'
    question = "Caption this image."

    model, tokenizer = load_trol(link=link)

    # move model to GPU
    for param in model.parameters():
        if not param.is_cuda:
            param.data = param.to('cuda:0')

    # prepare input prompt
    image_token_number = None
    if prompt_type == 'with_image':
        # load image
        image = pil_to_tensor(Image.open(img_path).convert("RGB"))
        if not "3.8B" in link:
            image_token_number = 1225
            image = F.interpolate(image.unsqueeze(0), size=(490, 490), mode='bicubic').squeeze(0)
        inputs = [{'image': image, 'question': question}]
    elif prompt_type == 'text_only':
        inputs = [{'question': question}]

    # generate response
    with torch.inference_mode():
        _inputs = model.eval_process(inputs=inputs,
                                     data='demo',
                                     tokenizer=tokenizer,
                                     device='cuda:0',
                                     img_token_number=image_token_number)
        generate_ids = model.generate(**_inputs, max_new_tokens=256, use_cache=True)
        response = output_filtering(tokenizer.batch_decode(generate_ids, skip_special_tokens=False)[0], model)
    print(response)

if __name__ == "__main__":
    main()
