import deepzoom
import PIL.Image
import os
import shutil

##########
# https://stackoverflow.com/questions/579310/formatting-long-numbers-as-strings-in-python
def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])
##########

# This entire script is super messy
# To use with your own tsne image, modify: INPUT_TSNE_IMAGE, OUTPUT_DIR, TSNE_FILES_NAME

overwrite = True
resolution = 20000
num_patches = 4096
patch_px = 128
perp = 30
grid = '_grid'
test = '_test'
tsne_LR = 200
hum_resolution = human_format(resolution)

INPUT_TSNE_IMAGE = "/mnt/data/projects-hubert/VIDI/embedding_visualization/"+\
                    "tsne{}_{}x{}_{}px_{}LR_{}perp_border-color{}.png".format(test,
                                                                              hum_resolution,
                                                                              hum_resolution,
                                                                              patch_px,
                                                                              tsne_LR,
                                                                              perp,
                                                                              grid)

OUTPUT_DIR = "tsne{}_visualization_{}x{}_{}px_{}LR_{}perp_{}patches_border-color{}".format(test,
                                                                        hum_resolution,
                                                                        hum_resolution,
                                                                        patch_px,
                                                                        tsne_LR,
                                                                        perp,
                                                                        num_patches,
                                                                        grid)

print("==== Writing output to: ====")
print(OUTPUT_DIR)
print("overwrite: {}".format(overwrite))
print("dir exists: {}".format(os.path.exists(OUTPUT_DIR)))
print("============================")
if os.path.exists(OUTPUT_DIR):
    if not overwrite:
        raise Exception("Set overwrite to True to overwrite existing directory!")
    else:
        shutil.rmtree(OUTPUT_DIR)
os.makedirs(OUTPUT_DIR)

### Create DeepZoom Tiles. ###
PIL.Image.MAX_IMAGE_PIXELS = 13151043584
creator = deepzoom.ImageCreator(tile_size=256, tile_overlap=1, tile_format="jpg",
                                image_quality=0.8, resize_filter="bilinear")
TSNE_FILES_NAME = "tsne_{}x{}_{}px".format(hum_resolution,
                                           hum_resolution,
                                           patch_px)
creator.create(INPUT_TSNE_IMAGE, os.path.join(OUTPUT_DIR, TSNE_FILES_NAME+".dzi"))

### Create Embedding HTML. ###
embedding_html_template = open("embedding_template.html", "r")
lines = []
template_repl = {"<<TSNE_FILES_PATH>>": TSNE_FILES_NAME+"_files/",
                "<<HEIGHT>>": resolution,
                "<<WIDTH>>": resolution,
                }
template_repl = {k:str(v) for k,v in template_repl.items()}

for line in embedding_html_template:
    for key in template_repl:
        line = line.replace(key, template_repl[key])
    # print(line)
    lines.append(line)

outfp = open(os.path.join(OUTPUT_DIR, "embedding.html"), "w+")
outfp.write("".join(lines))


