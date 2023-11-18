from PIL import Image
import numpy as np
import pandas as pd
import time

def rgb_to_hsv(img_path):
    PI_3 = 60
    rgb = np.array((Image.open(img_path)).convert('RGB'))/255
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    Cmax = np.max(rgb, axis=2)
    Cmin = np.min(rgb, axis=2)
    delta = Cmax - Cmin

    h = np.where(delta == 0, 
                0, np.where(r == Cmax, PI_3 * (np.divide((g - b), delta) %  6), 
                np.where(g == Cmax, PI_3 * (np.divide((b - r), delta) + 2), PI_3 * (np.divide((r - g), delta) + 4))))

    s = np.where(Cmax == 0, 0, np.where(Cmax != 0, delta/Cmax, 0))
    v = Cmax

    h0 = np.logical_or(np.logical_and(316 <= h, h <= 360), h<1)
    h1 = np.logical_and(1 <= h, h <= 25)
    h2 = np.logical_and(26 <= h, h <= 40)
    h3 = np.logical_and(41 <= h , h <= 120)
    h4 = np.logical_and(121 <= h, h <= 190)
    h5 = np.logical_and(191 <= h, h <= 270)
    h6 = np.logical_and(271 <= h, h <= 295)
    h = np.where( h0, 0, np.where(h1, 1, 
                np.where(h2, 2, np.where(h3, 3, 
                np.where(h4, 4, np.where(h5, 5, np.where(h6, 6, 7)))))))

    s0 = np.logical_and(0 <= s, s < 0.2)
    s1 = np.logical_and(0.2 <= s, s < 0.7)

    v0 = np.logical_and(0 <= v, v < 0.2)
    v1 = np.logical_and(0.2 <= v, v < 0.7)

    s = np.where(s0, 0, np.where(s1, 1, 2))

    v = np.where(v0, 0, np.where(v1, 1, 2))


    matrix = np.stack((h, s, v), axis=-1)
    nineblock = [np.array_split(row, 4, 1) for row in np.array_split(matrix, 4)]
    return nineblock

def cosine_similiarity_color(A, B):
    resfinal = []
    arr_weight = [0.05, 0.05, 0.05, 0.05, 0.05, 0.1, 0.1, 0.05, 0.05, 0.1, 0.1, 0.05, 0.05, 0.05, 0.05, 0.05]
    for i in range(3):
        res1 = []
        for j in range(16):
            AB1 = np.dot(A[j][i], B[j][i])
            A21 = np.sqrt(np.dot(A[j][i], A[j][i]))
            B21 = np.sqrt(np.dot(B[j][i], B[j][i]))
            res1.append(AB1/(A21*B21))
        res = np.dot(res1, arr_weight)
        resfinal.append(res)
    return (np.mean(resfinal))   
 
def histogram(block): # one dimensional, h, s, atau v
    histblock = []
    for i in range(4):
        for j in range(4):
            histh1, _ = np.histogram(block[i][j][:,:,0], bins=[0,1,2,3,4,5,6,7,8])
            hists1, _ = np.histogram(block[i][j][:,:,1], bins=[0,1,2,3])
            histv1, _ = np.histogram(block[i][j][:,:,2], bins=[0,1,2,3])
            size = block[i][j][:,:,0].size
            histblock1 = (histh1/size, hists1/size, histv1/size)
            histblock.append(histblock1)
    return (histblock)