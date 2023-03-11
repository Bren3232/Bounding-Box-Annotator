
# Just to test bbox annotator make sure the boxx is correct

import cv2

img_path = "path/to/image"

img = cv2.imread(img_path)

if img_path.startswith("../"):
    img_path = img_path[2:]

box = img_path.split(".")
print(box)
box = box[0].split("_")

sx = int(box[-4])
sy = int(box[-3])
ex = int(box[-2])
ey = int(box[-1])

print(box[-4:])

cv2.rectangle(img, (sx, sy), (ex, ey), [22, 255, 88], 2)

cv2.imshow("rect", img)
cv2.waitKey(0)
