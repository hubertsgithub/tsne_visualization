import numpy as np
from sklearn.manifold import TSNE
import os

INPUT_DIR =  "/mnt/data/projects-hubert/VIDI/classifier/features"
# INPUT_DIR =  "/mnt/data/projects-hubert/VIDI/classifier/features_test"
features_path = os.path.join(INPUT_DIR, "features.npz")
image_paths_file = os.path.join(INPUT_DIR, "image_paths.tsv")


OUTPUT_DIR = "features_tsne"
# OUTPUT_DIR = "features_tsne_test"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

features = np.load(features_path)['features']
image_paths = np.array(open(image_paths_file).readlines())

assert (len(features) == len(image_paths))

shuffled_idxs = np.arange(len(features))
np.random.shuffle(shuffled_idxs)


# Subsample these features to save some time.
features = features[shuffled_idxs]
features = features[:4096]
print(features.shape)

image_paths = image_paths[shuffled_idxs]
image_paths = image_paths[:4096]
print(image_paths.shape)

image_paths = [ip.strip() for ip in image_paths]
fp = open(os.path.join(OUTPUT_DIR, 'images_TSNE.txt'), "w+")
fp.write("\n".join(image_paths))
fp.close()


LR_list = [200]#, 10]
components = [2] #,3]
perps = [5, 30, 50]
for perp in perps:
    for n_components in components:
        for LR in LR_list:
            features_TSNE = TSNE(n_components=n_components, learning_rate=LR,
                                perplexity=perp, verbose=10, n_jobs=28, n_iter=5000).fit_transform(features)
            print(features_TSNE.shape)
            np.savez(os.path.join(OUTPUT_DIR, 'features_TSNE_{}D_{}LR_{}perp.npz'.format(n_components,LR,perp)),
                    features=features_TSNE)



