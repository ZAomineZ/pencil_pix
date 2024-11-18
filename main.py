import numpy as np
import imageio.v2 as imageio  # Using v2 to avoid warnings
import scipy.ndimage
import cv2


def rgb_to_gray(rgb_image):
    """
    Converts an RGB image to grayscale.
    """
    return np.dot(rgb_image[..., :3], [0.2989, 0.5870, 0.1140])


def dodge(front, back):
    """
    Applies the "dodge" effect to create a sketch-like appearance.
    """
    result = front * 255 / (255 - back)
    result[result > 255] = 255
    result[back == 255] = 255
    return result.astype('uint8')


def create_sketch(input_image_path, output_image_path, blur_sigma=13):
    """
    Converts an image into a sketch and saves it.

    Args:
        input_image_path (str): Path to the input image.
        output_image_path (str): Path to save the output sketch image.
        blur_sigma (int, optional): Gaussian blur intensity. Default is 13.
    """
    # Load the image
    image = imageio.imread(input_image_path)

    # Convert to grayscale
    gray_image = rgb_to_gray(image)

    # Invert the colors
    inverted_image = 255 - gray_image

    # Apply Gaussian blur
    blurred_image = scipy.ndimage.gaussian_filter(inverted_image, sigma=blur_sigma)

    # Create the sketch using the dodge effect
    sketch = dodge(blurred_image, gray_image)

    # Save the resulting sketch image
    cv2.imwrite(output_image_path, sketch)


if __name__ == '__main__':
    # Parameters for execution
    input_image = 'test.jpeg'
    output_image = 'test_coloring.png'

    # Generate the sketch
    create_sketch(input_image, output_image)
