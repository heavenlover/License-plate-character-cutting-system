import numpy as np
import cv2
if __name__ == "__main__":
    # 原始图像路径(根据文件改路径)
    path = '1.jpg'
    # 读取图像
    img = cv2.imread(path)
    # 第一步 : 缩放图像到指定大小 (320, 100)
    img1 = cv2.resize(img, (320, 100), interpolation=cv2.INTER_AREA)
    # 第二步 : 将图像转换为灰度图像
    img2 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    # 第三步 : 使用双边滤波去除噪声，保留边缘信息
    img3 = cv2.bilateralFilter(img2, 11, 17, 17)
    # 第四步 : 使用Canny算法提取图像的纹理信息（边缘检测）
    img4 = cv2.Canny(img3, 50, 150)
    # 第五步 : 裁剪图像，去除边缘部分，保留中间区域
    img5 = img4[10:90, 10:310]
    # 同时裁剪原始缩放图像，用于后续绘制分割框
    crop_img = img1[10:90, 10:310, :]
    # 查找轮廓，使用RETR_EXTERNAL模式只检测外轮廓
    contours, hierarchy = cv2.findContours(img5, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    candidate = []
    # 遍历所有轮廓，筛选出符合条件的候选区域
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        # 对轮廓的面积和宽高进行筛选，去除不合理的部分
        if w * h < 500:
            continue
        if w * h > 4000:
            continue
        if h < 20:
            continue
        if w > 80:
            continue
        # 保存候选区域的起始和结束x坐标
        candidate.append([x, (x + w)])
    # 初始化一个长度为300的数组，用于标记候选区域
    loc = np.zeros(300)
    # 标记候选区域
    for j in range(len(candidate)):
        x1 = candidate[j][0]
        x2 = candidate[j][1]
        loc[x1:x2] = 1
    # 初始化字符的起始和结束坐标列表
    start = []
    end = []
    # 确定字符的起始和结束坐标
    if loc[0] == 1:
        start.append(0)
    for j in range(300 - 1):
        if loc[j] == 0 and loc[j + 1] == 1:
            start.append(j)
        if loc[j] == 1 and loc[j + 1] == 0:
            end.append(j)
    if loc[299] == 1:
        end.append(299)
    # 绘制字符分割框
    cv2.rectangle(crop_img, (0, 0), (start[1] - 5, 80), (0, 0, 255), 2)
    for j in range(1, 7):
        x1 = start[j]
        x2 = end[j]
        y1 = 0
        y2 = 80
        cv2.rectangle(crop_img, (x1, y1), (x2, y2), (0, 0, 255), 2)
    # 显示最终的裁剪图像
    cv2.namedWindow("final_crop_img")
    cv2.imshow("final_crop_img", crop_img)
    cv2.waitKey(0)
