## CNN + CSP Sudoku-Solver

This project is based on [OpenCV Sudoku Solver](https://www.pyimagesearch.com/2020/08/10/opencv-sudoku-solver-and-ocr/)


### 文件组织

```
├── cnn.py            # CNN模型，实现，训练
├── eval.py           # 检查模型提取的特征图
├── load_mnist.py     # 加载mnist中的数据集
├── mnist             # 打包过后的原数据集
├── process_cn_deprecated.py  # 处理CN数据集的第一步
├── process_cn_new.py         # 处理CN数据集的第二步
├── solve_sudoku_puzzle.py    # 数独求解框架，参数model, image, debug 
├── sudoku_images             # 创建CN数据集时使用的脚本
│   └── collect_digit_pict.py
├── sudoku_solver.py          # CSP实现
├── train_res
└── utils             # 保存的模型
    ├── __init__.py
    ├── mnist_test_utils.py  # 带加粗的数字提取脚本
    └── puzzle_utils.py      # 原框架的数字提取脚本
```