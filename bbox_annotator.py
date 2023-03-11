
# Collects bounding box points and stores them in the corresponding image names.
# Hit "z" to undo, will remove the bbox points from the image name and goto previous image
# By Brendan Murphy, b-murphy.ca


import cv2
import imutils as im
import os
import select_aoi

path_img_dir = "../bbox_clamp/anno_test"

imgs_names_list = os.listdir(path_img_dir)
print("Number of images in folder: ", len(imgs_names_list))   # number of files in folder

split_dir = os.path.split(path_img_dir)
print(split_dir)

resize = 800

new_imgn_list = []
idx = 0

while True:

    if idx >= len(imgs_names_list):
        print("===> Reached end of imgs")
        break

    print("Image ", idx + 1)

    img = cv2.imread(os.path.join(path_img_dir, imgs_names_list[idx]))

    img_w = img.shape[1]

    if resize > 0:
        img = im.resize(img, resize)

    # My select AOI return start pt and end pt, does not need adding like selectROI
    bbox = select_aoi.select_aoi_bbox(window_name="select aoi", img=img, crosshairs=True, rect_thickness=1,
                                      rect_color=[0, 255, 0], crosshairs_thickness=1, crosshairs_color=[0, 0, 188])

    # bbox = select_aoi.select_circle_aoi(window_name="select aoi", img=img, crosshairs=True, circle_thickness=2,
    #                              circle_color=[0, 255, 0], crosshairs_thickness=1, crosshairs_color=[0, 0, 188])

    # Undo operation
    if bbox == False:
        idx -= 1

        if len(new_imgn_list) < 1:
            print("===> At image 1, can't go back any further")
            idx += 1
            continue

        last_img_name, ex = new_imgn_list[-1].split(".")
        new_imgn_list = new_imgn_list[:-1]

        lins = last_img_name.split("_")
        n = last_img_name.find(f'_{lins[-4]}_{lins[-3]}_{lins[-2]}_{lins[-1]}')

        os.rename(os.path.join(path_img_dir,f'{last_img_name}.{ex}'),
                  os.path.join(path_img_dir, f'{last_img_name[:n]}.{ex}'))
        continue

    if resize > 0:
        scal = img_w / resize
        for idx2, i in enumerate(bbox):
            bbox[idx2] = int(i * scal)

    nam = imgs_names_list[idx].split(".")
    new_name = f'{nam[0]}_{bbox[0]}_{bbox[1]}_{bbox[2]}_{bbox[3]}.{nam[1]}'
    os.rename(os.path.join(path_img_dir, imgs_names_list[idx]),
              os.path.join(path_img_dir, new_name))

    new_imgn_list.append(new_name)

    idx += 1

cv2.destroyAllWindows()

