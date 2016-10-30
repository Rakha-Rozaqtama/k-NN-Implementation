# k-NN-Implementation

k-NN is a supervised, lazy algorithm that compares incoming test data with training data to find similar instances, using which test data is classified. For a given test instance, the algorithm searches for k number of closest instances/neighbors from training data. Once this set of closest instances is obtained, the class label occurring most number of times is assigned to the test instance; ties are broken arbitrarily.

The three distance/similarity measures implemented here are,

1. Euclidean distance:
Is the ordinary, straight-line distance between two given points.
2. Polynomial kernel:
Is defined by k(x, y) = (x*y + 1) ^ d where d is the degree of the polynomial and is specified by the kernel degree parameter. These kernels are well suited for problems where all the training data is normalized.
3. Radial basis kernel:
Is defined by k(x, y) = exp{((-|| x – y ||) ^ 2) / (sigma ^ 2)}. Sigma is an adjustable parameter and plays a major role in the performance of the kernel, and should be carefully tuned to the problem at hand. For this implementation 0.97 is found to be resulting in good accuracy.

Following are the sources for the three datasets that were used to test the implementation and its classification accuracy,

1. https://archive.ics.uci.edu/ml/machine-learning-databases/ecoli/ecoli.names
2. https://archive.ics.uci.edu/ml/datasets/Glass+Identification
3. https://archive.ics.uci.edu/ml/datasets/Yeast

Input to the code:

1. Dataset
2. Count of folds (k) for k-fold cross validation
3. Number of nearest neighbors i.e. k-NN

Output:

1. Each record/instance and respective prediction
2. Overall accuracy for each type of distance/similarity measure
