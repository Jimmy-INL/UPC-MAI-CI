import os
import scipy.misc
import numpy as np

from model import DCGAN
from utils import pp, visualize, to_json

import tensorflow as tf

flags = tf.app.flags
flags.DEFINE_integer("epoch", 100, "Epoch to train [25]")
flags.DEFINE_float("learning_rate", 0.0002, "Learning rate of for adam [0.0002]")
flags.DEFINE_float("beta1", 0.5, "Momentum term of adam [0.5]")
flags.DEFINE_integer("train_size", np.inf, "The size of train images [np.inf]")
flags.DEFINE_integer("batch_size", 64, "The size of batch images [64]")
flags.DEFINE_integer("image_size", 108, "The size of image to use (will be center cropped) [108]")
flags.DEFINE_integer("output_size", 64, "The size of the output images to produce [64]")
flags.DEFINE_integer("c_dim", 3, "Dimension of image color. [3]")
flags.DEFINE_string("dataset", "celebA", "The name of dataset [celebA, mnist, lsun]")
flags.DEFINE_string("checkpoint_dir", "checkpoint", "Directory name to save the checkpoints [checkpoint]")
flags.DEFINE_string("sample_dir", "samples", "Directory name to save the image samples [samples]")
flags.DEFINE_boolean("is_train", False, "True for training, False for testing [False]")
flags.DEFINE_boolean("is_crop", False, "True for training, False for testing [False]")
flags.DEFINE_boolean("visualize", False, "True for visualizing, False for nothing [False]")

flags.DEFINE_integer("d", 8, "Digit to be generated")
flags.DEFINE_integer("k", 5000, "Number of real samples to be used")
FLAGS = flags.FLAGS

def main(_):
    pp.pprint(flags.FLAGS.__flags)

    if not os.path.exists(FLAGS.checkpoint_dir):
        os.makedirs(FLAGS.checkpoint_dir)
    if not os.path.exists(FLAGS.sample_dir):
        os.makedirs(FLAGS.sample_dir)

    with tf.Session() as sess:
        if FLAGS.dataset == 'mnist':
            dcgan = DCGAN(sess,
                          image_size=FLAGS.image_size,
                          batch_size=FLAGS.batch_size,
                          y_dim=10,
                          output_size=28,
                          c_dim=1,
                          dataset_name=FLAGS.dataset,
                          is_crop=FLAGS.is_crop,
                          checkpoint_dir=FLAGS.checkpoint_dir,
                          sample_dir=FLAGS.sample_dir,
                          d=FLAGS.d,
                          k=FLAGS.k)
        else:
            dcgan = DCGAN(sess,
                          image_size=FLAGS.image_size,
                          batch_size=FLAGS.batch_size,
                          output_size=FLAGS.output_size,
                          c_dim=FLAGS.c_dim,
                          dataset_name=FLAGS.dataset,
                          is_crop=FLAGS.is_crop,
                          checkpoint_dir=FLAGS.checkpoint_dir,
                          sample_dir=FLAGS.sample_dir)

        if FLAGS.is_train:
            dcgan.train(FLAGS)
        else:
            dcgan.load(FLAGS.checkpoint_dir)


        OPTION = 0
        visualize(sess, dcgan, FLAGS, OPTION, FLAGS.d, FLAGS.sample_dir)

if __name__ == '__main__':
    tf.app.run()
