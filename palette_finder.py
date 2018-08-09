import cv2
import numpy as np

from sklearn import cluster


def get_histogram(model):
    num_labels = np.arange(0, len(np.unique(model.labels_)) + 1)
    hist, bin_edges = np.histogram(model.labels_, bins=num_labels, density=1)
    return hist


def plot_colors(hist, model, height=720, width=360):

    #sort data in non-decreasing order
    palette = model.cluster_centers_.astype(int)
    palette = palette[(-hist).argsort()]
    hist = hist[(-hist).argsort()]

    #create palette bars
    bar = np.zeros((height, width, 3), dtype = "uint8")
    start = 0

    for (percent, color) in zip(hist, palette):
        end = start + (percent * height)
        cv2.rectangle(bar, (0, int(start)), (width, int(end)),
                color.astype("uint8").tolist(), -1)
        start = end

    return bar


def get_palette(filename, n_colors=5):
    save_file='tmp_palette.jpg'
    image = cv2.imread(filename)
    image = image.reshape((image.shape[0] * image.shape[1], 3))

    #cluster pixels using k-means
    model = cluster.KMeans(n_clusters=n_colors)
    model.fit(image)
    hist = get_histogram(model)
    bar = plot_colors(hist, model)
    cv2.imwrite(save_file, bar)

    return save_file


def format_images(img_names, width=3):
    save_file='tweet_img.jpg'
    images = [cv2.imread(f) for f in img_names]
    
    height = images[0].shape[0]
    bar = np.zeros((height, width, 3), dtype = "uint8")
    cv2.rectangle(bar, (0, 0), (width, height), (255, 255, 255), -1)
    images.insert(1, bar)
    new_image = np.concatenate(images, axis=1)
    cv2.imwrite(save_file, new_image)

    return save_file
    

def main():
    img_file = './images/sample.jpg'
    palette_file = get_palette(img_file)
    tweet_img = format_images([img_file, palette_file])
    print('Image saved in current directory as {}'.format(tweet_img))


if __name__ == "__main__":
    main()

