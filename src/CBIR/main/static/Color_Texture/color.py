from PIL import Image
import numpy as np
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
    nineblock = [np.array_split(row, 3, 1) for row in np.array_split(matrix, 3)]
    # print(nineblock[0][0].shape)
    # print(block[0][0][:,:,1])
    return nineblock
def cosine_similiarity_color(A, B):
    resfinal = []
    for i in range(3):
        AB1 = np.dot(A[0][i], B[0][i])
        A21 = np.sqrt(np.dot(A[0][i], A[0][i]))
        B21 = np.sqrt(np.dot(B[0][i], B[0][i]))
        res1 = AB1/(A21*B21)

        AB2 = np.dot(A[1][i], B[1][i])
        A22 = np.sqrt(np.dot(A[1][i], A[1][i]))
        B22 = np.sqrt(np.dot(B[1][i], B[1][i]))
        res2 = AB2/(A22*B22)
        
        AB3 = np.dot(A[2][i], B[2][i])
        A23 = np.sqrt(np.dot(A[2][i], A[2][i]))
        B23 = np.sqrt(np.dot(B[2][i], B[2][i]))
        res3 = AB3/(A23*B23)
        
        AB4 = np.dot(A[3][i], B[3][i])
        A24 = np.sqrt(np.dot(A[3][i], A[3][i]))
        B24 = np.sqrt(np.dot(B[3][i], B[3][i]))
        res4 = AB4/(A24*B24)
        
        AB5 = np.dot(A[4][i], B[4][i])
        A25 = np.sqrt(np.dot(A[4][i], A[4][i]))
        B25 = np.sqrt(np.dot(B[4][i], B[4][i]))
        res5 = AB5/(A25*B25)

        AB6 = np.dot(A[5][i], B[5][i])
        A26 = np.sqrt(np.dot(A[5][i], A[5][i]))
        B26 = np.sqrt(np.dot(B[5][i], B[5][i]))
        res6 = AB6/(A26*B26)

        AB7 = np.dot(A[6][i], B[6][i])
        A27 = np.sqrt(np.dot(A[6][i], A[6][i]))
        B27 = np.sqrt(np.dot(B[6][i], B[6][i]))
        res7 = AB7/(A27*B27)

        AB8 = np.dot(A[7][i], B[7][i])
        A28 = np.sqrt(np.dot(A[7][i], A[7][i]))
        B28 = np.sqrt(np.dot(B[7][i], B[7][i]))
        res8 = AB8/(A28*B28)

        AB9 = np.dot(A[8][i], B[8][i])
        A29 = np.sqrt(np.dot(A[8][i], A[8][i]))
        B29 = np.sqrt(np.dot(B[8][i], B[8][i]))
        res9 = AB9/(A29*B29)

        res = (res1 + res2 + res3 + res4 + res5 + res6 + res7 + res8 + res9)/9
        resfinal.append(res)
    # print(resfinal) 
    return (np.mean(resfinal))   
 
def histogram(block): # one dimensional, h, s, atau v
    histh1, _ = np.histogram(block[0][0][:,:,0], bins=[0,1,2,3,4,5,6,7,8])
    hists1, _ = np.histogram(block[0][0][:,:,1], bins=[0,1,2,3])
    histv1, _ = np.histogram(block[0][0][:,:,2], bins=[0,1,2,3])
    size = block[0][0][:,:,0].size
    histblock1 = (histh1/size, hists1/size, histv1/size)
    # np.concatenate((histh1, hists1, histv1))

    histh2, _ = np.histogram(block[0][1][:,:,0], bins=[0,1,2,3,4,5,6,7,8])
    hists2, _ = np.histogram(block[0][1][:,:,1], bins=[0,1,2,3])
    histv2, _ = np.histogram(block[0][1][:,:,2], bins=[0,1,2,3])
    size = block[0][1][:,:,0].size
    histblock2 = (histh2/size, hists2/size, histv2/size)
    # np.concatenate((histh2, hists2, histv2))

    histh3, _ = np.histogram(block[0][2][:,:,0], bins=[0,1,2,3,4,5,6,7,8])
    hists3, _ = np.histogram(block[0][2][:,:,1], bins=[0,1,2,3])
    histv3, _ = np.histogram(block[0][2][:,:,2], bins=[0,1,2,3])
    size = block[0][2][:,:,0].size
    histblock3 = (histh3/size, hists3/size, histv3/size)
    # np.concatenate((histh3, hists3, histv3))

    histh4, _ = np.histogram(block[1][0][:,:,0], bins=[0,1,2,3,4,5,6,7,8])
    hists4, _ = np.histogram(block[1][0][:,:,1], bins=[0,1,2,3])
    histv4, _ = np.histogram(block[1][0][:,:,2], bins=[0,1,2,3])
    size = block[1][0][:,:,0].size
    histblock4 = (histh4/size, hists4/size, histv4/size)
    # np.concatenate((histh4, hists4, histv4))

    histh5, _ = np.histogram(block[1][1][:,:,0], bins=[0,1,2,3,4,5,6,7,8])
    hists5, _ = np.histogram(block[1][1][:,:,1], bins=[0,1,2,3])
    histv5, _ = np.histogram(block[1][1][:,:,2], bins=[0,1,2,3])
    size = block[1][1][:,:,0].size
    histblock5 = (histh5/size, hists5/size, histv5/size)
    # np.concatenate((histh5, hists5, histv5))

    histh6, _ = np.histogram(block[1][2][:,:,0], bins=[0,1,2,3,4,5,6,7,8])
    hists6, _ = np.histogram(block[1][2][:,:,1], bins=[0,1,2,3])
    histv6, _ = np.histogram(block[1][2][:,:,2], bins=[0,1,2,3])
    size = block[1][2][:,:,0].size
    histblock6 = (histh6/size, hists6/size, histv6/size)
    # np.concatenate((histh6, hists6, histv6))

    histh7, _ = np.histogram(block[2][0][:,:,0], bins=[0,1,2,3,4,5,6,7,8])
    hists7, _ = np.histogram(block[2][0][:,:,1], bins=[0,1,2,3])
    histv7, _ = np.histogram(block[2][0][:,:,2], bins=[0,1,2,3])
    size = block[2][0][:,:,0].size
    histblock7 = (histh7/size, hists7/size, histv7/size)
    # np.concatenate((histh7, hists7, histv7))

    histh8, _ = np.histogram(block[2][1][:,:,0], bins=[0,1,2,3,4,5,6,7,8])
    hists8, _ = np.histogram(block[2][1][:,:,1], bins=[0,1,2,3])
    histv8, _ = np.histogram(block[2][1][:,:,2], bins=[0,1,2,3])
    size = block[2][1][:,:,0].size
    histblock8 = (histh8/size, hists8/size, histv8/size)
    # np.concatenate((histh8, hists8, histv8))

    histh9, _ = np.histogram(block[2][2][:,:,0], bins=[0,1,2,3,4,5,6,7,8])
    hists9, _ = np.histogram(block[2][2][:,:,1], bins=[0,1,2,3])
    histv9, _ = np.histogram(block[2][2][:,:,2], bins=[0,1,2,3])
    size = block[2][2][:,:,0].size
    histblock9 = (histh9/size, hists9/size, histv9/size)
    # np.concatenate((histh9, hists9, histv9))
    return (histblock1,histblock2,histblock3,histblock4,histblock5,histblock6,histblock7,histblock8,histblock9)

# starttime = time.time()
# img_path = '948_1.jpg'
# img_path2 = '354_0.jpg'
# nineblock = rgb_to_hsv(img_path)
# nineblock2 = rgb_to_hsv(img_path2)
# sim = cosine_similarity(histogram(nineblock), histogram(nineblock2))*100
# print(""+str(round(sim, 2)), end='')
# print("%")

# endtime = time.time()
# print(endtime - starttime)

# res = []