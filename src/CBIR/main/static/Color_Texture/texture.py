from PIL import Image
import numpy as np
from numpy.linalg import norm
import time

def texture(img_path):
    # Open Image
    rgb = np.array(Image.open(img_path).convert('RGB'))

    # Vektor Pengali RGB
    P = np.array([0.29, 0.587, 0.114])

    # Matrix Grayscale
    Y = np.dot(rgb, P).astype(np.uint8)
    
    # Matrix Co-Occurence
    (h, w) = Y.shape
    MatrixOcc = np.zeros((256, 256), dtype='i')
    for i in range(h):
        for j in range(w-1):
            MatrixOcc[Y[i, j], Y[i, j+1]] += 1
    
    # Matrix Symmetric & GLCM
    Sym = MatrixOcc + MatrixOcc.transpose()
    Sym = np.divide(Sym, np.sum(Sym))

    
    # Hitung Contrast, Homoogeneity, dan Entropy
    index = np.arange(Sym.shape[0])
    Contrast = np.sum(np.square(index[:, None] - index) * Sym)
    Homogeneity = np.sum(Sym / (1 + np.square(index[:, None] - index)))
    Entropy = -np.sum(np.where(Sym == 0, 0, Sym * np.log(Sym)))
    return np.array([Contrast, Homogeneity, Entropy])

def cosine_similiarity(V1, V2):
    return np.dot(V1, V2)/(norm(V1)*norm(V2))
# def main():
#     path1 = 'putih2_0.png'
#     path2 = 'apel_0.jpg'
#     V1 = texture(path1)
#     print(V1)
#     V2 = texture(path2)
#     print(V2)
#     print("%.10f" % cosine_similiarity(V1,V2))

# start = time.time()
# main()
# end = time.time()
# print("time:", end - start)

