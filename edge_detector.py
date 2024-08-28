import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread("images\simple_track.png",0)
edges = cv2.Canny(img,50,50)

indices = np.where(edges != [0])
coordinates = zip(indices[0], indices[1])



titles = ['track 1 image', "edges"]

images = [img, edges]

for i in range(2):
    plt.subplot(1,2,i+1),plt.imshow(images[i],'grey')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])

plt.show()