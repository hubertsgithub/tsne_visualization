import numpy as np
import multiprocessing
from functools import partial
import PIL.Image
import tqdm

############
#https://sashat.me/2017/01/11/list-of-20-simple-distinct-colors/
CAT_TO_BORDER_COLOR = {
        "ceramic": np.array((250, 190, 190)),
        "fabric": np.array((145, 30, 180)),
        "foliage": np.array((60, 180, 75)),
        "glass": np.array((70, 240, 240)),
        "liquid": np.array((0, 130, 200)),
        "metal": np.array((128, 128, 128)),
        "paper": np.array((255, 250, 200)),
        "skin": np.array((255, 215, 180)),
        "stone": np.array((255, 225, 25)),
        "wood": np.array((170, 110, 40)),
}

def construct_tsne_image(i, image_paths, patch_size=(224,224),
                         border_color=False, border_size=None):
    '''
    image_path: path to 224x224 patch.
    tsne_feature: 2D tsne projection of patch feature.
    '''
    patch = np.array(PIL.Image.open(image_paths[i]).resize(patch_size))
    if border_color:
        if border_size is None:
            border_size = patch_size[0] // 20
        cat = image_paths[i].split("/")[-2]
        assert cat in CAT_TO_BORDER_COLOR.keys()
        color = CAT_TO_BORDER_COLOR[cat]
        patch[:border_size, :] = color
        patch[:, :border_size] = color
        patch[-border_size:, :] = color
        patch[:, -border_size:] = color
    return (i,patch)
############

perp = 5
tsne_LR = 200
TEST = False
SNAP_TO_GRID = True

if TEST:
    tsne = np.load("features_tsne_test/features_TSNE_2D_{}LR_{}perp.npz".format(tsne_LR, perp))['features']
    image_paths = np.array([l.strip() for l in open("features_tsne_test/images_TSNE.txt").readlines()])
else:
    tsne = np.load("features_tsne/features_TSNE_2D_{}LR_{}perp.npz".format(tsne_LR, perp))['features']
    image_paths = np.array([l.strip() for l in open("features_tsne/images_TSNE.txt").readlines()])
print(image_paths[0])

### Create grid, just do some heuristic scaling and overlap images.
GRID_SIZE = np.array((20000, 20000, 3))
if TEST:
    PATCH_SIZE = np.array((224,224))
else:
    PATCH_SIZE = np.array((128,128))

tsne -= np.min(tsne, axis=0)
scale_factor = (GRID_SIZE[:2]-PATCH_SIZE) / np.max(tsne, axis=0)
tsne *= scale_factor
tsne = tsne.astype(np.int)

tsne_image = np.zeros(GRID_SIZE, dtype=np.uint8)
print(tsne_image.shape)

pool = multiprocessing.Pool(28)
mp_func = partial(construct_tsne_image,
                image_paths=image_paths,
                patch_size=PATCH_SIZE,
                border_color=True,
                )
assert tsne.shape[0] == image_paths.shape[0], (tsne.shape, image_paths.shape)
mp_input = range(tsne.shape[0])

for i, patch in tqdm.tqdm(pool.imap_unordered(mp_func, mp_input), total=tsne.shape[0]):
    if SNAP_TO_GRID:
        x_snapped = (tsne[i][0] // patch.shape[0]) * patch.shape[0]
        y_snapped = (tsne[i][1] // patch.shape[1]) * patch.shape[1]
        x_slice = slice(x_snapped,x_snapped+patch.shape[0])
        y_slice = slice(y_snapped,y_snapped+patch.shape[1])
    else:
        x_slice = slice(tsne[i][0],tsne[i][0]+patch.shape[0])
        y_slice = slice(tsne[i][1],tsne[i][1]+patch.shape[1])
    tsne_image[x_slice, y_slice] = patch

if TEST:
    savename = "tsne_test_20Kx20K_{}px_{}LR_{}perp_border-color.png".format(PATCH_SIZE[0], tsne_LR, perp)
else:
    savename = "tsne_20Kx20K_{}px_{}LR_{}perp_border-color.png".format(PATCH_SIZE[0], tsne_LR, perp)
if SNAP_TO_GRID:
    savename = savename.replace(".png", "_grid.png")
PIL.Image.fromarray(tsne_image).save(savename)
print("Saving to: {}".format(savename))

