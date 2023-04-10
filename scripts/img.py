# https://github.com/openai/openai-cookbook/blob/main/examples/dalle/Image_generations_edits_and_variations_with_DALL-E.ipynb
import PIL.ImageShow
import openai
import requests
import os
from PIL import Image

openai.api_key = os.environ.get("OPENAI_API_KEY")

image_dir_name = "images"
image_dir = os.path.join(os.curdir, image_dir_name)
if not os.path.isdir(image_dir):
    os.mkdir(image_dir)
print(f"{image_dir=}")

# create an image

# set the prompt
prompt = "A cyberpunk monkey hacker dreaming of a beautiful bunch of bananas, digital art"

# call the OpenAI API
generation_response = openai.Image.create(
    prompt=prompt,
    n=1,
    size="1024x1024",
    response_format="url",
)

# print response
print(generation_response)


# save the image
generated_image_name = "generated_image.png"  # any name you like; the filetype should be .png
generated_image_filepath = os.path.join(image_dir, generated_image_name)
generated_image_url = generation_response["data"][0]["url"]  # extract image URL from response
generated_image = requests.get(generated_image_url).content  # download the image

with open(generated_image_filepath, "wb") as image_file:
    image_file.write(generated_image)  # write the image to the file

# print the image
print(generated_image_filepath)
# display(Image.open(generated_image_filepath))
# PIL.ImageShow.DisplayViewer().show_file(path=generated_image_filepath)
#PIL.ImageShow.DisplayViewer().show_image(image=Image.open(generated_image_filepath))
img = Image.open(generated_image_filepath)
# img.show()


################################ create variations

# call the OpenAI API, using `create_variation` rather than `create`
variation_response = openai.Image.create_variation(
    image=generated_image,  # generated_image is the image generated above
    n=2,
    size="1024x1024",
    response_format="url",
)

# print response
print(variation_response)

# save the images
variation_urls = [datum["url"] for datum in variation_response["data"]]  # extract URLs
variation_images = [requests.get(url).content for url in variation_urls]  # download images
variation_image_names = [f"variation_image_{i}.png" for i in range(len(variation_images))]  # create names
variation_image_filepaths = [os.path.join(image_dir, name) for name in variation_image_names]  # create filepaths
for image, filepath in zip(variation_images, variation_image_filepaths):  # loop through the variations
    with open(filepath, "wb") as image_file:  # open the file
        image_file.write(image)  # write the image to the file

# print the original image
print(generated_image_filepath)
# display(Image.open(generated_image_filepath))
# Image.open(generated_image_filepath).show()

# print the new variations
for variation_image_filepaths in variation_image_filepaths:
    print(variation_image_filepaths)
    # display(Image.open(variation_image_filepaths))
    # Image.open(variation_image_filepaths).show()


################################ Edit

# create a mask
width = 1024
height = 1024
mask = Image.new("RGBA", (width, height), (0, 0, 0, 1))  # create an opaque image mask

# set the bottom half to be transparent
for x in range(width):
    for y in range(height // 2, height):  # only loop over the bottom half of the mask
        # set alpha (A) to zero to turn pixel transparent
        alpha = 0
        mask.putpixel((x, y), (0, 0, 0, alpha))

# save the mask
mask_name = "bottom_half_mask.png"
mask_filepath = os.path.join(image_dir, mask_name)
mask.save(mask_filepath)

# edit an image

# call the OpenAI API
edit_response = openai.Image.create_edit(
    image=open(generated_image_filepath, "rb"),  # from the generation section
    mask=open(mask_filepath, "rb"),  # from right above
    prompt=prompt,  # from the generation section
    n=1,
    size="1024x1024",
    response_format="url",
)

# print response
print(edit_response)

# save the image
edited_image_name = "edited_image.png"  # any name you like; the filetype should be .png
edited_image_filepath = os.path.join(image_dir, edited_image_name)
edited_image_url = edit_response["data"][0]["url"]  # extract image URL from response
edited_image = requests.get(edited_image_url).content  # download the image

with open(edited_image_filepath, "wb") as image_file:
    image_file.write(edited_image)  # write the image to the file

# print the original image
print(generated_image_filepath)
# display(Image.open(generated_image_filepath))
Image.open(generated_image_filepath).show()

# print edited image
print(edited_image_filepath)
# display(Image.open(edited_image_filepath))
Image.open(edited_image_filepath).show()
