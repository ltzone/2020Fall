import argparse

import imutils
import cv2

from pyimagesearch.sudoku import puzzle

OUTPUT_DIR = "dataset/my/"


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
                    help="path to read input image")
    ap.add_argument("-l", "--label", required=True,
                    help="label of the input image 0~9")
    ap.add_argument("-d", "--debug", type=int, default=-1,
                    help="whether or not we are visualizing each step of the pipeline")
    args = vars(ap.parse_args())

    # load the input image from disk and resize it
    print("[INFO] processing image...")
    image = cv2.imread(args["image"])
    image = imutils.resize(image, width=600)

    # find the puzzle in the image and then
    (puzzleImage, warped) = puzzle.find_puzzle(image, debug=args["debug"] > 0)

    stepX = warped.shape[1] // 9
    stepY = warped.shape[0] // 9

    # loop over the grid locations
    total_cnt = 0
    for y in range(0, 9):
        for x in range(0, 9):
            # compute the starting and ending (x, y)-coordinates of the
            # current cell
            startX = x * stepX
            startY = y * stepY
            endX = (x + 1) * stepX
            endY = (y + 1) * stepY

            # crop the cell from the warped transform image and then
            # extract the digit from the cell
            cell = warped[startY:endY, startX:endX]
            digit = puzzle.extract_digit(cell, debug=args["debug"] > 0)

            # verify that the digit is not empty
            if digit is not None:
                # resize the cell to 28x28 pixels and then prepare the
                # cell for classification
                roi = cv2.resize(digit, (28, 28))
                out_path = OUTPUT_DIR+args["label"]+"/"+str(total_cnt)+".png"
                cv2.imwrite(out_path, roi)
                # roi = roi.astype("float") / 255.0
                # roi = img_to_array(roi)
                # roi = np.expand_dims(roi, axis=0)
                total_cnt += 1
    print(total_cnt)
