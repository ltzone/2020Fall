# USAGE
# python solve_sudoku_puzzle.py --model train/res1 --image sudoku_images/sudoku_puzzle.jpg

# import the necessary packages
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from utils.puzzle_utils import *
import numpy as np
import argparse
import imutils
import cv2
import os
from sudoku_solver import SudokuSolution

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# SHOW_MAP = {
#     1:"1", 2:"2", 3:"3", 4:"4", 5:"5", 6:"6", 7:"7", 8:"8", 9:"9", 0:"",
#     10:"十", 11:"一", 12:"二", 13:"三", 14:"四", 15:"五", 16:"六",
#     17:"七", 18:"八", 19:"九"
# }

SHOW_MAP = {
    1:"1", 2:"2", 3:"3", 4:"4", 5:"5", 6:"6", 7:"7", 8:"8", 9:"9", 0:"",
    10:"0", 11:"1", 12:"2", 13:"3", 14:"4", 15:"5", 16:"6",
    17:"7", 18:"8", 19:"9"
}


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True,
                help="path to trained digit classifier")
ap.add_argument("-i", "--image", required=True,
                help="path to input sudoku puzzle image")
ap.add_argument("-d", "--debug", type=int, default=-1,
                help="whether or not we are visualizing each step of the pipeline")
args = vars(ap.parse_args())

# load the digit classifier from disk
print("[INFO] loading digit classifier...")
model = load_model(args["model"])

# load the input image from disk and resize it
print("[INFO] processing image...")
image = cv2.imread(args["image"])
image = imutils.resize(image, width=600)

# find the puzzle in the image and then
(puzzleImage, warped) = find_puzzle(image, debug=args["debug"] > 0)

# initialize our 9x9 sudoku board
board = np.zeros((9, 9), dtype="int")

# a sudoku puzzle is a 9x9 grid (81 individual cells), so we can
# infer the location of each cell by dividing the warped image
# into a 9x9 grid
stepX = warped.shape[1] // 9
stepY = warped.shape[0] // 9

# initialize a list to store the (x, y)-coordinates of each cell
# location
cellLocs = []

# loop over the grid locations
for y in range(0, 9):
    # initialize the current list of cell locations
    row = []

    for x in range(0, 9):
        # compute the starting and ending (x, y)-coordinates of the
        # current cell
        startX = x * stepX
        startY = y * stepY
        endX = (x + 1) * stepX
        endY = (y + 1) * stepY

        # add the (x, y)-coordinates to our cell locations list
        row.append((startX, startY, endX, endY))

        # crop the cell from the warped transform image and then
        # extract the digit from the cell
        cell = warped[startY:endY, startX:endX]
        digit = extract_digit(cell, debug=args["debug"] > 0)

        # verify that the digit is not empty
        if digit is not None:
            foo = np.hstack([cell, digit])
            if (args["debug"]>0):
                cv2.imshow("Cell/Digit", foo)
                cv2.waitKey(0)

            # resize the cell to 28x28 pixels and then prepare the
            # cell for classification
            roi = cv2.resize(digit, (28, 28))
            roi = roi.astype("float32") / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            # classify the digit and update the sudoku board with the
            # prediction
            print(roi)
            # pred_results = model.predict(roi)
            pred_results = model.predict(np.around(roi))
            pred = pred_results.argmax(axis=1)[0]
            print(pred_results, pred)
            board[y, x] = pred

    # add the row to our cell locations
    cellLocs.append(row)

# loop over the cell locations and board
for i, cellRow in enumerate(cellLocs):
    # loop over individual cell in the row
    for j, box in enumerate(cellRow):
        if board[i][j] == 0:
            continue
        # unpack the cell coordinates
        startX, startY, endX, endY = box

        # compute the coordinates of where the digit will be drawn
        # on the output puzzle image
        textX = int((endX - startX) * 0.33)
        textY = int((endY - startY) * -0.2)
        textX += startX
        textY += endY

        # draw the result digit on the sudoku puzzle image
        cv2.putText(puzzleImage, str(board[i,j]), (textX, textY),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)

# show the output image
cv2.imshow("Recognition Result", puzzleImage)
cv2.waitKey(0)

# construct a sudoku puzzle from the board
print("[INFO] OCR'd sudoku board:")
print(board)
puzzle = SudokuSolution(board)

# solve the sudoku puzzle
print("[INFO] solving sudoku puzzle...")
solution = puzzle.solve()
print(solution)

# loop over the cell locations and board
for i, (cellRow, boardRow) in enumerate(zip(cellLocs, solution)):
    # loop over individual cell in the row
    for j, (box, digit) in enumerate(zip(cellRow, boardRow)):
        # unpack the cell coordinates
        startX, startY, endX, endY = box

        # compute the coordinates of where the digit will be drawn
        # on the output puzzle image
        textX = int((endX - startX) * 0.33)
        textY = int((endY - startY) * -0.2)
        textX += startX
        textY += endY

        show_digit = SHOW_MAP[digit]

        # draw the result digit on the sudoku puzzle image
        if board[i][j] != 0: # known digits
            cv2.putText(puzzleImage, str(show_digit), (textX, textY),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)
        else:
            cv2.putText(puzzleImage, str(show_digit), (textX, textY),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

# show the output image
cv2.imshow("Sudoku Result", puzzleImage)
cv2.waitKey(0)
