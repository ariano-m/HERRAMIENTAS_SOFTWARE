"""
    Adrián Riaño Martínez
    Hoja de problemas 1
    Ejercicio 1
     python data_augmentation.py --input_dataset=../datasets/tiny-imagenet-200/test/images
                                 --factor=20 --output_dataset=./augmented_tiny_imagenet
"""

from PIL import ImageFilter as image_filter
from PIL import Image as pil
from tqdm import tqdm
import argparse
import random
import glob
import os


def generate_transform(image):
    """
        function for generating random transformations to images
    :param image:
    :return:
    """
    def resize(im):
        """
            resize image
        :param im:
        :return:
        """
        width, height = image.size
        resize = random.uniform(0.25, 2.5)
        resize_t = (int(width * resize), int(height * resize))
        return im.resize(resize_t)

    def filter(im):
        """
            filter image using blur
        :param im:
        :return:
        """
        blur = random.randrange(2, 10)   # random value blur
        return im.filter(image_filter.GaussianBlur(blur))

    def transformate(im):
        """
            apply a random rotation and flips to image
        :param im:
        :return:
        """
        funcs_pillow = [pil.FLIP_LEFT_RIGHT,   # all transformations operations
                        pil.FLIP_TOP_BOTTOM,
                        pil.ROTATE_90,
                        pil.ROTATE_180,
                        pil.ROTATE_270,
                        pil.TRANSPOSE,
                        pil.TRANSVERSE]
        action = random.randrange(0, 6)   # random choose
        return im.transpose(method=funcs_pillow[action])

    func_l = [resize, filter, transformate]
    for _ in range(random.randrange(1, 4)):  # random number of operations
        fun = func_l[random.randint(0, 2)]  # random operation
        image = fun(image)

    return image


def main(args):
    input_dataset = args['input_dataset']   # read args
    output_dataset = args['output_dataset']
    factor = args['factor']

    if not os.path.isdir(input_dataset):
        raise Exception("This path doesn't exit")

    if input_dataset[-1] != '/':
        input_dataset += '/'

    new_images = []
    images = glob.glob(input_dataset + '*.JPEG')
    for image in tqdm(images):
        image_pil = pil.open(image)
        img_l = [generate_transform(image_pil) for _ in range(factor)]
        new_images.extend(img_l)

    if not os.path.exists(output_dataset):
        os.makedirs(output_dataset)

    if output_dataset[-1] != '/':
        output_dataset += '/'

    print("Saving all images...")
    for idx, im in tqdm(enumerate(new_images)):
        im.save(output_dataset + f'image_{idx}.jpeg')


if __name__ == "__main__":
    desc = 'data augmentation script'
    parser = argparse.ArgumentParser(description=desc)

    commom_params = {'type': str, 'nargs': 1, 'required': True}
    parser.add_argument('--input_dataset', help='source with images', **commom_params)
    parser.add_argument('--output_dataset', help='dataset with augmentation', **commom_params)
    parser.add_argument('--factor', type=int, nargs=1, required=True, help='dataset with augmentation')

    args = {i: j[0] for i, j in vars(parser.parse_args()).items() if j is not None}

    main(args)
