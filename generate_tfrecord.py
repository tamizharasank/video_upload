"""
Usage:
  # From tensorflow/models/
  # Create train data:
  python generate_tfrecord.py --csv_input=data/train_labels.csv  --output_path=train.record

  # Create test data:
  python generate_tfrecord.py --csv_input=data/test_labels.csv  --output_path=test.record
"""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import io
import pandas as pd
import tensorflow as tf

import sys

sys.path.append('models/research/object_detection')
from PIL import Image
from object_detection.utils import dataset_util

from collections import namedtuple, OrderedDict

flags = tf.app.flags
flags.DEFINE_string('csv_input', '', 'Path to the CSV input')
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
flags.DEFINE_string('file_name','','filename of a model')
FLAGS = flags.FLAGS


# TO-DO replace this with label map
def class_text_to_int(row_label):
    n=FLAGS.file_name
    if row_label == row_label:
    	s=row_label.split("_")[::-1][0]
    	s=int(s)
        return s
    else:
        None


def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]


def create_tf_example(group, path):
    with tf.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    width, height = image.size

    filename = group.filename.encode('utf8')
    image_format = b'jpg'
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []

    for index, row in group.object.iterrows():
        xmins.append(row['xmin'] / width)
        xmaxs.append(row['xmax'] / width)
        ymins.append(row['ymin'] / height)
        ymaxs.append(row['ymax'] / height)
        classes_text.append(row['class'].encode('utf8'))
        classes.append(class_text_to_int(row['class']))

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
    output_path = os.path.join(os.getcwd(), FLAGS.output_path)
    fn=output_path.split("/")[::-1][2]
    # print(fn)
    oo=output_path.split("/")[::-1][0]
    if (oo.split(".")[0])=='test':
        
        writer = tf.python_io.TFRecordWriter(FLAGS.output_path)
        path = os.path.join(os.getcwd(), 'static/img/upload/video/training/{}/images/test'.format(fn))
        examples = pd.read_csv(FLAGS.csv_input)
        grouped = split(examples, 'filename')
        for group in grouped:
            tf_example = create_tf_example(group, path)
            writer.write(tf_example.SerializeToString())

        writer.close()
        output_path = os.path.join(os.getcwd(), FLAGS.output_path)
        print('Successfully created the TFRecords: {}'.format(output_path))
        # n=FLAGS.file_name
        # print(type(n))        
        # print(oo.split(".")[0])
    else:
        writer = tf.python_io.TFRecordWriter(FLAGS.output_path)
        path = os.path.join(os.getcwd(), 'static/img/upload/video/training/{}/images/train'.format(fn))
        examples = pd.read_csv(FLAGS.csv_input)
        grouped = split(examples, 'filename')
        for group in grouped:
            tf_example = create_tf_example(group, path)
            writer.write(tf_example.SerializeToString())

        writer.close()
        output_path = os.path.join(os.getcwd(), FLAGS.output_path)
        
        print('Successfully created the TFRecords: {}'.format(output_path))        
        # print(oo.split(".")[0])
        # n=FLAGS.file_name
        # print(n)


if __name__ == '__main__':
    tf.app.run()