import io
import tensorflow as tf
import csv
from object_detection.utils import dataset_util
from PIL import Image
import numpy as np
import cv2

flags = tf.app.flags
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
flags.DEFINE_string('input_csv', '', 'Path to input CSV')
flags.DEFINE_string('img_dir', '', 'Path to image dataset')
FLAGS = flags.FLAGS

def class_text_to_int(row_label):
    if row_label == 'Damage':
        return 1
    else:
        None


def create_tf_example(example):
    # TODO(user): Populate the following variables from your example.

    height = int(example[2]) # Image height
    width = int(example[1]) # Image width
    filename = example[0].encode('utf8') # Filename of the image. Empty if image is not from file

    with tf.gfile.GFile('./images/train/'+example[0]+'.jpg', 'rb') as fid:
        encoded_jpg = fid.read()

    encoded_jpg_io = io.BytesIO(encoded_jpg)

    image_format = b'jpg'

    xmins = [int(example[4])] # List of normalized left x coordinates in bounding box (1 per box)
    xmaxs = [int(example[6])] # List of normalized right x coordinates in bounding box
                # (1 per box)
    ymins = [int(example[5])] # List of normalized top y coordinates in bounding box (1 per box)
    ymaxs = [int(example[7])] # List of normalized bottom y coordinates in bounding box
                # (1 per box)
    classes_text = [example[3].encode('utf8')] # List of string class name of bounding box (1 per box)
    classes = [1] # List of integer class id of bounding box (1 per box)

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))
    return tf_example


def main(_):
    writer = tf.python_io.TFRecordWriter(FLAGS.output_path)
    csvfile = FLAGS.input_csv
    imagedir = FLAGS.img_dir
    # TODO(user): Write code to read in your dataset to examples variable
    with open(csvfile, 'r') as f:
        examples = csv.reader(f)
        examples = list(examples)[1:]

    for example in range(len(examples)):
        print (example)
        tf_example = create_tf_example(examples[example])
        writer.write(tf_example.SerializeToString())

    writer.close()

if __name__ == '__main__':
    tf.app.run()