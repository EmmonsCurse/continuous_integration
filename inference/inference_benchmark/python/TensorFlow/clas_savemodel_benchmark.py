import argparse
import os
import sys
import time
import logging

import numpy as np
import tensorflow as tf  # tf version should greater than 2.3.0

from tensorflow.python.compiler.tensorrt import trt_convert as trt
from tensorflow.python.saved_model import tag_constants

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)
logger.info("==== Tensorflow version: {} ====".format(tf.version.VERSION))


def parse_args():
    """
    parse input args
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, help="model name")
    parser.add_argument(
        "--model_path", type=str, help="model save model input path")
    parser.add_argument(
        "--trt_precision",
        type=str,
        default="fp32",
        help="trt precision, choice = ['fp32', 'fp16', 'int8']")
    parser.add_argument(
        "--image_shape",
        type=str,
        default="3,224,224",
        help="can only use for one input model(e.g. image classification)")

    parser.add_argument("--use_gpu", dest="use_gpu", action='store_true')
    parser.add_argument("--use_trt", dest="use_trt", action='store_true')
    parser.add_argument("--use_xla", dest="use_xla", action='store_true')

    parser.add_argument("--batch_size", type=int, default=1, help="batch size")
    parser.add_argument("--warmup_times", type=int, default=5, help="warmup")
    parser.add_argument("--repeats", type=int, default=1000, help="repeats")

    return parser.parse_args()

def benchmark_tftrt(args):
    input_saved_model = args.model_path
    saved_model_loaded = tf.saved_model.load(
        input_saved_model, tags=[tag_constants.SERVING])
    infer = saved_model_loaded.signatures['serving_default']

    channels = int(args.image_shape.split(',')[0])
    height = int(args.image_shape.split(',')[1])
    width = int(args.image_shape.split(',')[2])
    logger.info("channels: {0}, height: {1}, width: {2}".format(channels,
                                                                height, width))
    input_shape = (args.batch_size, height, width, channels)

    if args.use_gpu:
        run_device = '/gpu:0'
    else:
        run_device = '/cpu:0'
    logger.warn("=== tf.device cannot specify device correctly ===")
    with tf.device(run_device):
        batched_input = tf.constant(np.ones(input_shape).astype("float"))
        batched_input = tf.cast(batched_input, dtype="float")

        for i in range(args.warmup_times):
            labeling = infer(batched_input)

        time1 = time.time()
        for i in range(args.repeats):
            labeling = infer(batched_input)
        time2 = time.time()
        total_inference_cost = (time2 - time1) * 1000  # total latency, ms

    return total_inference_cost


def summary_config(args, infer_time: float):
    """
    Args:
        args : input args
        infer_time : inference time
    """
    logger.info("----------------------- Model info ----------------------")
    logger.info("Model name: {0}, Model type: {1}".format(args.model_name,
                                                          "keras_dy2static"))
    logger.info("----------------------- Data info -----------------------")
    logger.info("Batch size: {0}, Num of samples: {1}".format(args.batch_size,
                                                              args.repeats))
    logger.info("----------------------- Conf info -----------------------")
    logger.info("device: {0}".format("gpu" if args.use_gpu else "cpu"))
    if (args.use_gpu):
        logger.info("enable_tensorrt: {0}".format(args.use_trt))
        if (args.use_trt):
            logger.info("trt_precision: {0}".format(args.trt_precision))
    logger.info("enable_xla: {0}".format(args.use_xla))
    logger.info("----------------------- Perf info -----------------------")
    logger.info("Average latency(ms): {0}, QPS: {1}".format(
        infer_time / args.repeats, (args.repeats * args.batch_size) / (
            infer_time / 1000)))


def run_demo():
    """
    run_demo
    """
    args = parse_args()
    total_time = benchmark_tftrt(args)
    summary_config(args, total_time)


if __name__ == "__main__":
    run_demo()
