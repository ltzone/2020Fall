import numpy as np
import imutils
import cv2
from imutils.perspective import four_point_transform
from skimage.segmentation import clear_border


def find_puzzle(image, debug=False):
    # convert the image to grayscale and blur it slightly
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 3)

    # apply adaptive thresholding and then invert the threshold map
    thresh = cv2.adaptiveThreshold(blurred, 255,
                                   cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    thresh = cv2.bitwise_not(thresh)

    # check to see if we are visualizing each step of the image
    # processing pipeline (in this case, thresholding)
    if debug:
        cv2.imshow("Puzzle Thresh", thresh)
        cv2.waitKey(0)

    # find contours in the thresholded image and sort them by size in
    # descending order
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    # initialize a contour that corresponds to the puzzle outline
    puzzle_cnt = None

    # loop over the contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        # if our approximated contour has four points, then we can
        # assume we have found the outline of the puzzle
        if len(approx) == 4:
            puzzle_cnt = approx
            break

    # if the puzzle contour is empty then our script could not find
    # the outline of the sudoku puzzle so raise an error
    if puzzle_cnt is None:
        raise Exception(("Could not find sudoku puzzle outline. "
                         "Try debugging your thresholding and contour steps."))

    # check to see if we are visualizing the outline of the detected
    # sudoku puzzle
    if debug:
        # draw the contour of the puzzle on the image and then display
        # it to our screen for visualization/debugging purposes
        output = image.copy()
        cv2.drawContours(output, [puzzle_cnt], -1, (0, 255, 0), 2)
        cv2.imshow("Puzzle Outline", output)
        cv2.waitKey(0)

    # apply a four point perspective transform to both the original
    # image and grayscale image to obtain a top-down birds eye view
    # of the puzzle
    puzzle = four_point_transform(image, puzzle_cnt.reshape(4, 2))
    warped = four_point_transform(gray, puzzle_cnt.reshape(4, 2))

    # check to see if we are visualizing the perspective transform
    if debug:
        # show the output warped image (again, for debugging purposes)
        cv2.imshow("Puzzle Transform", puzzle)
        cv2.waitKey(0)

    # return a 2-tuple of puzzle in both RGB and grayscale
    return puzzle, warped


def extract_digit(cell, debug=False):
    # apply automatic thresholding to the cell and then clear any
    # connected borders that touch the border of the cell
    thresh = cv2.threshold(cell, 0, 255,
                           cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # This is new!
    # resize the picture, bolden the digit and eliminate border
    # SCALE_FACTOR = 1
    # scaled_height = int(thresh.shape[0] * SCALE_FACTOR)
    # scaled_width = int(thresh.shape[1] * SCALE_FACTOR)
    # top_pad = int((scaled_height - thresh.shape[0]) / 2)
    # left_pad = int((scaled_width - thresh.shape[1]) / 2)
    # big_mask = np.zeros((scaled_height, scaled_width), dtype="uint8")
    # big_mask = cv2.resize(thresh, big_mask.shape)
    # thresh = big_mask[top_pad:top_pad + thresh.shape[0], left_pad:left_pad + thresh.shape[1]]
    thresh = clear_border(thresh)

    # check to see if we are visualizing the cell thresholding step
    if debug:
        cv2.imshow("Cell Thresh", thresh)
        cv2.waitKey(0)

    # find contours in the thresholded cell
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # if no contours were found than this is an empty cell
    if len(cnts) == 0:
        return None

    # otherwise, find the largest contour in the cell and create a
    # mask for the contour
    c = max(cnts, key=cv2.contourArea)
    mask = np.zeros(thresh.shape, dtype="uint8")
    cv2.drawContours(mask, [c], -1, 255, -1)

    # otherwise, find contours large enough in the cell and create a
    # mask for the contour
    # mask = np.zeros(thresh.shape, dtype="uint8")
    # cv2.drawContours(mask, cnts, -1, 255, -1)

    # if debug:
    #     cv2.imshow("Mask", mask)
    #     cv2.waitKey(0)


    # compute the percentage of masked pixels relative to the total
    # area of the image
    (h, w) = thresh.shape
    percent_filled = cv2.countNonZero(mask) / float(w * h)

    # if less than 1% of the mask is filled then we are looking at
    # noise and can safely ignore the contour
    if percent_filled < 0.01:
        return None

    # apply the mask to the thresholded cell
    digit = cv2.bitwise_and(thresh, thresh, mask=mask)

    # bolden
    left_digit = np.roll(digit, 1, axis=0)
    right_digit = np.roll(digit, -1, axis=0)
    top_digit = np.roll(digit, 1, axis=1)
    bot_digit = np.roll(digit, -1, axis=1)
    x_bolden_digit = cv2.bitwise_or(left_digit, right_digit)
    y_bolden_digit = cv2.bitwise_or(top_digit, bot_digit)
    digit = cv2.bitwise_or(digit, x_bolden_digit)
    digit = cv2.bitwise_or(digit, y_bolden_digit)

    # check to see if we should visualize the masking step
    if debug:
        cv2.imshow("Digit", digit)
        cv2.waitKey(0)

    # return the digit to the calling function
    return digit
