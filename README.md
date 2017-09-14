# neuralDraw
This is a gui for training and testing a digit detection system based on the neural network described in Tariq Rahid's book "Make your on neural network".

![Drawing](https://raw.githubusercontent.com/F4b1-/neuralDraw/master/readme_images/draw.png)


Prerequisites
------
The gui relies on [kivy](https://kivy.org/docs/installation/installation.html). The neural network makes use of _scipy_, _numpy_ and _matplotlib_. After installing the dependencies just run _neural_draw.py_.

General
------
This repository includes the gui and the neural network. It does not include the mnint test data however. You can get it [here](http://www.pjreddie.com/media/files/mnist_train.csv) and copy it to _mnist_dataset/mnist_train.csv_.
If you check the _Save in test data_ box, the result of your test will be added to _mnist_dataset/my_test_data.csv_. This data can later be used to improve your test data.

The weights for the network are provided in the _weights_who.npy_ and _weights_wih.npy_ files so the network does not need to be trained everytime you start the gui. Delete these files if you want to use a new set of training data.

![Correction](https://raw.githubusercontent.com/F4b1-/neuralDraw/master/readme_images/result.png)
![Correction](https://raw.githubusercontent.com/F4b1-/neuralDraw/master/readme_images/correct.png)



To-Do
------
- [ ] Make the training data file location editable in the gui
- [ ] Improve the process of saving, cropping and analyzing the drawing area
- [ ] Create a setup.py file

