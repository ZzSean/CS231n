import numpy as np
from random import shuffle
from past.builtins import xrange

def softmax_loss_naive(W, X, y, reg):
  """
  Softmax loss function, naive implementation (with loops)

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using explicit loops.     #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  num_train = X.shape[0]
  num_class = W.shape[1]
  score = np.dot(X, W)
  score -= np.max(score)
  for i in xrange(num_train):
    y_i = np.argmax(score[i,:])
    sum_e = np.sum(np.exp(score[i,:]))   
    for j in xrange(num_class):
      if j==y_i:
        dW[:,j] += -X[i,:] + np.exp(score[i, j])/sum_e*X[i,:]
      else:
        dW[:,j] += np.exp(score[i, j])/sum_e*X[i,:]
    loss += - score[i,y_i] + np.log(sum_e)
  loss /= num_train
  loss += 0.5 * reg * np.sum(W * W)
  dW /= num_train
  dW += reg * W 
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
  """
  Softmax loss function, vectorized version.

  Inputs and outputs are the same as softmax_loss_naive.
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################


  num_train = X.shape[0]
  score = np.dot(X, W)
  score -= np.max(score)
  loss = np.sum(-np.max(score, axis = 1) + np.log(np.sum(np.exp(score), axis = 1)))
  #score_index = np.argmax(score, axis = 1)
  matrix_1 = np.reshape(np.sum(np.exp(score), axis = 1), [num_train, 1])
  matrix_2 = np.exp(score)
  matrix_3 = matrix_2 / matrix_1
  matrix_3[np.arange(num_train), y] += -1
  dW = np.dot(X.T, matrix_3)
  #for i in xrange(num_train):
  # dW[:, y[i]] -= X[i]

  loss /= num_train
  loss += 0.5 * reg * np.sum(W * W)
  dW /= num_train
  dW += reg * W 
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW

