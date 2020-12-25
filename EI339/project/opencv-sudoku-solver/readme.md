## CNN + CSP Sudoku-Solver



### Experiments

MNIST
- `train/res1`
    - activation: sigmoid     
    - loss: 0.0243 
    - categorical_accuracy: 0.9834
- `res_en4_0.001_tanh`
    - epoch: 10
    - activation: tanh     
    - loss: 0.0264 
    - categorical_accuracy: 0.9828
- `res_en4_0.001_tanh_round`
    - epoch: 10
    - rounded to 0,1
    - activation: tanh     
    - loss: 0.0220 
    - categorical_accuracy: 0.9847

Mixed Dataset
- `train/res_mixed`
- loss: 0.0751 
- categorical_accuracy: 0.9632

CN Dataset
- `res/CN_classifier`
  - trained on filtered dataset
  - Structure: LeNet
  - 20 epoches, 100 batch size
  - train_accuracy: 0.9925, loss 0.0368
  - test_accuracy: 0.9222, loss 0.3103
  - can work on `test/p1.jpeg`
