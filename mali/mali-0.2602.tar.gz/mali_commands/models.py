# -*- coding: utf8 -*-

import click

from missinglink import KerasCallback, TensorFlowProject, PyCaffeCallback


KERAS = 'keras'
TENSORFLOW = 'tf'
PYTORCH = 'pytorch'
PYCAFFE = 'caffe'


@click.group('models')
def models_commands():
    pass


@models_commands.command('getWeightsHash')
@click.option('--framework', type=click.Choice([KERAS, TENSORFLOW, PYTORCH, PYCAFFE]), required=True)
@click.option('--model', type=click.Path(), required=True,
              help='The filepath of the saved model. For Caffe, provide the filepath of the model definition file')
@click.option('--weights', type=click.Path(), required=False,
              help='For Caffe only, the filepath of the saved weights')
@click.pass_context
def get_weights_hash(ctx, framework, model, weights):
    """Calculate the weights hash of the trained neural network.

    \b
    Keras
    -----

    The model's weights should be saved with its full structure e.g. by using the `ModelCheckpoint`
    callback with `save_weights_only=False` (default) or by explicitly calling `model.save(filepath)`.
    Assume that the model is saved as `checkpoint.hdf5`, to calculate the hash:

    \b
        mali models getWeightsHash --framework keras --model checkpoint.hdf5

    \b
    TensorFlow
    ----------

    The model can be saved using `tf.train.Saver` which would create at least 3 files: .meta,
    .index and .data files. These files need to be in the same directory when mali calculates the
    hash. Assume that we save the model with `saver.save(session, 'models/checkpoint.ckpt')`, to
    calculate the hash:

    \b
        mali models getWeightsHash --framework tf --model models/checkpoint.ckpt

    \b
    PyCaffe
    -------

    The model's weights can be saved in a `.caffemodel` file by using `net.save(filepath)` or
    `solver.snapshot` (which also saves the solver's state in another file). Assume that we have
    the train net's structure in `train.prototxt` and its weights saved in `checkpoint.caffemodel`,
    to calculate the hash:

    \b
        mali model getWeightsHash --framework caffe --model train.prototxt --weights checkpoints.caffemodel

    """
    if framework == KERAS:
        weights_hash = get_keras_weights_hash(model)

        # NOTE: there is a known issue when using Theano backend. There will be an exception printed out
        # https://github.com/pallets/click/issues/564
        click.echo(weights_hash)
    elif framework == TENSORFLOW:
        weights_hash = get_tensorflow_weights_hash(model)
        click.echo(weights_hash)
    elif framework == PYTORCH:
        click.echo('Support for PyTorch is coming soon :)')
    elif framework == PYCAFFE:
        if weights is None:
            raise click.BadOptionUsage('Please also specify --weights option for caffe model.')

        weights_hash = get_pycaffe_weights_hash(model, weights)
        click.echo(weights_hash)


def get_keras_weights_hash(model_filepath):
    try:
        import keras
    except ImportError:
        raise click.ClickException('Please install Keras library')

    if keras.backend.backend() == 'tensorflow':
        _disable_tensorflow_logging()

    try:
        import h5py
    except ImportError:
        raise click.ClickException("Please install h5py library for saving and loading Keras' models")

    model = keras.models.load_model(model_filepath)

    return KerasCallback.calculate_weights_hash(model)


def get_tensorflow_weights_hash(model_filepath):
    try:
        import tensorflow as tf
        _disable_tensorflow_logging()
    except ImportError:
        raise click.ClickException('Please install TensorFlow')

    with tf.Session() as session:
        model_meta_filepath = model_filepath + '.meta'
        saver = tf.train.import_meta_graph(model_meta_filepath)
        saver.restore(session, model_filepath)
        project = TensorFlowProject(None, None)
        with project.create_experiment() as exp:
            return exp.get_weights_hash(session)


def get_pycaffe_weights_hash(model_filepath, weights_filepath):
    try:
        # Need to be called before importing caffe
        _disable_caffe_logging()

        import caffe
    except ImportError:
        raise click.ClickException('Please install Caffe')

    net = caffe.Net(model_filepath, weights_filepath, caffe.TRAIN)

    return PyCaffeCallback.calculate_weights_hash(net)


def _disable_tensorflow_logging():
    import os
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def _disable_caffe_logging():
    import os
    os.environ['GLOG_minloglevel'] = '3'
