from __future__ import print_function
from tensorflow.python.util import compat
import numpy as np
import tfcoreml._shape_sensitive_layers as ss_layers
import tensorflow as tf

_SKIP_OP_TYPES = ['NoOp', 'ExpandDims', 'Cast', 'Squeeze']

def _is_skip_type(op):
  return op.type in _SKIP_OP_TYPES

def _backtrace_skip_ops(start_op):
  # if start_op is skippable, trace down its path to an unskippable op.
  op = start_op
  if not _is_skip_type(op):
    return op
  pred = None if len(op.inputs) == 0 else op.inputs[0].op
  while pred is not None and (_is_skip_type(pred)):
    op = pred
    pred = None if len(op.inputs) == 0 else op.inputs[0].op
  return pred

def add_tensor_sub(builder, name, x_name, y_name, output_name):
  y_out_name = 'negated_' + y_name + '_' + output_name
  builder.add_activation(y_out_name, 'LINEAR', y_name, y_out_name, [-1.0, 0])
  builder.add_elementwise(name, [x_name, y_out_name], output_name, 'ADD')

def add_tensor_div(builder, name, x_name, y_name, output_name):
  y_out_name = 'inversed_' + y_name + '_' + output_name
  builder.add_unary(y_out_name, y_name, y_out_name, 'inverse')
  builder.add_elementwise(name, [x_name, y_out_name], output_name, 'MULTIPLY')

def add_const(context, name, x, output_name, shape=None):
  ss_layers._add_const(context, name, x, output_name, shape)

def make_tensor(x, context):
  # returns tensor name, after converting input to a tensor, if the input is a
  # const or const-->identity
  if x.op.type == 'Const':
    add_const(context, x.name, context.consts[x.name], x.name)
  elif x.op.type == 'Identity' and x.op.inputs[0].name in context.consts:
    add_const(context, x.name, context.consts[x.op.inputs[0].name], x.name)
  return x.name


def placeholder(op, context):
  context.translated[compat.as_bytes(op.outputs[0].name)] = True
  try:
    inname = op.inputs[0].name
    # chain together no-ops here
    if inname in context.out_name_to_in_name:
      context.out_name_to_in_name[op.outputs[0].name] = (
          context.out_name_to_in_name[op.inputs[0].name])
    else:
      context.out_name_to_in_name[op.outputs[0].name] = op.inputs[0].name
  except:
    print('Skipping name of placeholder')

def identity(op, context):
  is_network_output = False
  for out in op.outputs:
    if out.name in context.output_names:
      is_network_output = True
      break
  input_name = compat.as_bytes(op.inputs[0].name)
  for out in op.outputs:
    output_name = compat.as_bytes(out.name)
    if op.inputs[0].op.type != 'Const':
      if is_network_output:
        context.builder.add_activation(
            output_name, 'LINEAR', input_name, output_name, [1.0, 0])
      else:
        skip(op, context)
    context.translated[output_name] = True

def batchnorm(op, context):

  input_name = compat.as_bytes(op.inputs[0].name)
  output_name = compat.as_bytes(op.outputs[0].name)
  num_channels = int(op.inputs[0].shape[-1])

  if op.type == 'BatchNormWithGlobalNormalization':
    mean = context.consts[compat.as_bytes(op.inputs[1].name)]
    variance = context.consts[compat.as_bytes(op.inputs[2].name)]
    beta = context.consts[compat.as_bytes(op.inputs[3].name)]
    gamma = context.consts[compat.as_bytes(op.inputs[4].name)]
    epsilon = op.get_attr('variance_epsilon')
  elif op.type == 'FusedBatchNorm':
    param_list = []
    for idx in range(1,5):
      if compat.as_bytes(op.inputs[idx].name) in context.consts:
        param_list.append(context.consts[compat.as_bytes(op.inputs[idx].name)])
      else:
        param_list.append(context.consts[compat.as_bytes(
            op.inputs[idx].op.inputs[0].name)])
    gamma, beta, mean, variance = param_list
    if mean.shape == (0,):
      mean = np.zeros((num_channels,))
    if variance.shape == (0,):
      variance = np.ones((num_channels,))
    epsilon = op.get_attr('epsilon')

  context.translated[output_name] = True
  context.builder.add_batchnorm(
      output_name, num_channels, gamma, beta, mean,
      variance, input_name, output_name, epsilon=epsilon)

def concat(op, context):
  ss_layers._add_concat(op, context)

def reshape(op, context):
  ss_layers._add_reshape(op, context)

def conv2d(op, context):
  x_name = compat.as_bytes(op.inputs[0].name)
  W_name = compat.as_bytes(op.inputs[1].name)
  output_name = compat.as_bytes(op.outputs[0].name)

  # Variables are sometimes 'read' via an Identity
  # Try to get the source of the Identity op if W is not already a constant
  if W_name in context.consts:
    W = context.consts[W_name]
  else:
    if _is_skip_type(op.inputs[1].op):
      identity_op = _backtrace_skip_ops(op.inputs[1].op)
    else:
      identity_op = op.inputs[1].op
    assert identity_op.type == 'Identity', (
        'Weight input has to be an identity op')
    W_name = compat.as_bytes(identity_op.inputs[0].name)
    assert W_name in context.consts, (
        'Value not found for {}'.format(W_name))
    W = context.consts[W_name]

  if op.type == 'QuantizedConv2D':
    assert op.inputs[4].name in context.consts, (
            'minimum value of quantized weights not available')
    assert op.inputs[5].name in context.consts, (
        'maximum value of quantized weights not available')
    min_W = context.consts[op.inputs[4].name]
    max_W = context.consts[op.inputs[5].name]
    if op.get_attr('Tfilter') == tf.quint8:
      W = ((max_W - min_W)/255.0) * W + min_W
    else:
      assert False, (
        'Only uint8 weights handled currently by the converter')

    context.translated[compat.as_bytes(op.outputs[1].name)] = True
    context.translated[compat.as_bytes(op.outputs[2].name)] = True

  inp_shape = context.shape_dict[x_name]
  out_shape = context.shape_dict[output_name]

  # Force W to be rank 4
  W_shape = [1]* (4-len(W.shape)) + list(W.shape)
  W = W.reshape(W_shape)

  kernelChannels = inp_shape[-1]
  outputChannels = out_shape[-1]
  height = W_shape[0]
  width = W_shape[1]
  strides = op.get_attr('strides')
  stride_height = strides[1]
  stride_width = strides[2]
  borderMode = op.get_attr('padding').lower()
  groups = 1
  b = None
  has_bias = False
  is_deconv = False
  output_shape = None
  input_name = x_name

  # dilated conv uses SpatialToBatchND as input; grab dilation rate there
  dilation_factors = [1, 1]

  if op.inputs[0].op.type == 'SpaceToBatchND':
    op1 = op.inputs[0].op
    dilation_factors = context.consts[op1.inputs[1].name]
    dilation_factors = list(dilation_factors.astype('int'))
  if op.inputs[0].op.type == 'ExpandDims' and \
      op.inputs[0].op.inputs[0].op.type == 'SpaceToBatchND':
    op1 = op.inputs[0].op.inputs[0].op
    df= context.consts[op1.inputs[1].name][0]
    dilation_factors[-1] = df

  context.builder.add_convolution(name=output_name,
                                  kernel_channels=kernelChannels,
                                  output_channels=outputChannels,
                                  height=height,
                                  width=width,
                                  stride_height=stride_height,
                                  stride_width=stride_width,
                                  border_mode=borderMode,
                                  groups=groups,
                                  W=W,
                                  b=b,
                                  has_bias=has_bias,
                                  is_deconv=is_deconv,
                                  output_shape=output_shape,
                                  input_name=input_name,
                                  output_name=output_name,
                                  dilation_factors=dilation_factors)
  context.translated[compat.as_bytes(op.outputs[0].name)] = True

def deconv2d(op, context):
  x_name = compat.as_bytes(op.inputs[2].name)
  W_name = compat.as_bytes(op.inputs[1].name)
  output_name = compat.as_bytes(op.outputs[0].name)
  if W_name in context.consts:
    W = context.consts[W_name]
  else:
    identity_op = op.inputs[1].op
    assert identity_op.type == 'Identity', (
        'Weight input has to be an identity op')
    W_name = compat.as_bytes(identity_op.inputs[0].name)
    assert W_name in context.consts, (
        'Value not found for {}'.format(W_name))
    W = context.consts[W_name]

  inp_shape = context.shape_dict[x_name]
  out_shape = context.shape_dict[output_name]

  W_shape = W.shape
  kernelChannels = inp_shape[-1]
  outputChannels = out_shape[-1]
  height = W_shape[0]
  width = W_shape[1]
  strides = op.get_attr('strides')
  stride_height = strides[1]
  stride_width = strides[2]
  borderMode = op.get_attr('padding').lower()
  groups = 1
  b = None
  has_bias = False
  is_deconv = True
  output_shape = None
  input_name = x_name
  context.builder.add_convolution(name=output_name,
                                  kernel_channels=kernelChannels,
                                  output_channels=outputChannels,
                                  height=height,
                                  width=width,
                                  stride_height=stride_height,
                                  stride_width=stride_width,
                                  border_mode=borderMode,
                                  groups=groups,
                                  W=np.transpose(W, (0, 1, 3, 2)),
                                  b=b,
                                  has_bias=has_bias,
                                  is_deconv=is_deconv,
                                  output_shape=output_shape,
                                  input_name=input_name,
                                  output_name=output_name)
  context.translated[compat.as_bytes(op.outputs[0].name)] = True

def avgpool(op, context):
  x_name = compat.as_bytes(op.inputs[0].name)
  output_name = compat.as_bytes(op.outputs[0].name)

  inp_shape = context.shape_dict[x_name]
  # Unlike conv that uses width axis for 1D computation,
  # Tensorflow uses height axis for 1D pooling. For 1D case we need to swap
  # height and width.
  is_1d = (inp_shape[1] > 1 and inp_shape[2] == 1)

  W_shape = op.get_attr('ksize')
  height = W_shape[2] if is_1d else W_shape[1]
  width = W_shape[1] if is_1d else W_shape[2]
  strides = op.get_attr('strides')
  stride_height = strides[2] if is_1d else strides[1]
  stride_width = strides[1] if is_1d else strides[2]
  borderMode = op.get_attr('padding')
  context.builder.add_pooling(name=output_name,
                              height=height,
                              width=width,
                              stride_height=stride_height,
                              stride_width=stride_width,
                              layer_type='AVERAGE',
                              padding_type=borderMode,
                              exclude_pad_area=True,
                              is_global=False,
                              input_name=x_name,
                              output_name=output_name)

  context.translated[compat.as_bytes(op.outputs[0].name)] = True

def maxpool(op, context):
  x_name = compat.as_bytes(op.inputs[0].name)
  output_name = compat.as_bytes(op.outputs[0].name)

  inp_shape = context.shape_dict[x_name]

  is_1d = (inp_shape[1] > 1 and inp_shape[2] == 1)

  W_shape = op.get_attr('ksize')
  height = W_shape[2] if is_1d else W_shape[1]
  width = W_shape[1] if is_1d else W_shape[2]
  strides = op.get_attr('strides')
  stride_height = strides[2] if is_1d else strides[1]
  stride_width = strides[1] if is_1d else strides[2]
  borderMode = op.get_attr('padding')
  context.builder.add_pooling(name=output_name,
                              height=height,
                              width=width,
                              stride_height=stride_height,
                              stride_width=stride_width,
                              layer_type='MAX',
                              padding_type=borderMode,
                              exclude_pad_area=True,
                              is_global=False,
                              input_name=x_name,
                              output_name=output_name)

  context.translated[compat.as_bytes(op.outputs[0].name)] = True

def depthwise_conv2d(op, context):
  x_name = compat.as_bytes(op.inputs[0].name)
  W_name = compat.as_bytes(op.inputs[1].name)
  output_name = compat.as_bytes(op.outputs[0].name)

  if W_name in context.consts:
    W = context.consts[W_name]
  else:
    identity_op = op.inputs[1].op
    assert identity_op.type == 'Identity', (
        'Weight input has to be an identity op')
    W_name = compat.as_bytes(identity_op.inputs[0].name)
    assert W_name in context.consts, (
        'Value not found for {}'.format(W_name))
    W = context.consts[W_name]

  W = np.transpose(W, (0, 1, 3, 2))

  inp_shape = context.shape_dict[x_name]
  out_shape = context.shape_dict[output_name]

  W_shape = W.shape
  kernelChannels = 1
  outputChannels = out_shape[-1]
  height = W_shape[0]
  width = W_shape[1]
  strides = op.get_attr('strides')
  stride_height = strides[1]
  stride_width = strides[2]
  borderMode = op.get_attr('padding').lower()
  groups = inp_shape[-1]
  b = None
  has_bias = False
  is_deconv = False
  output_shape = out_shape
  input_name = x_name
  context.builder.add_convolution(name=output_name,
                                  kernel_channels=kernelChannels,
                                  output_channels=outputChannels,
                                  height=height,
                                  width=width,
                                  stride_height=stride_height,
                                  stride_width=stride_width,
                                  border_mode=borderMode,
                                  groups=groups,
                                  W=W,
                                  b=b,
                                  has_bias=has_bias,
                                  is_deconv=is_deconv,
                                  output_shape=output_shape,
                                  input_name=input_name,
                                  output_name=output_name)
  context.translated[compat.as_bytes(op.outputs[0].name)] = True

def inner_product(op, context):
  x_name = compat.as_bytes(op.inputs[0].name)
  W_name = compat.as_bytes(op.inputs[1].name)
  output_name = compat.as_bytes(op.outputs[0].name)

  if W_name in context.consts:
    W = context.consts[W_name]
  else:
    identity_op = op.inputs[1].op
    assert identity_op.type == 'Identity', (
        'Weight input has to be an identity op')
    W_name = compat.as_bytes(identity_op.inputs[0].name)
    assert W_name in context.consts, (
        'Value not found for {}'.format(W_name))
    W = context.consts[W_name]
  assert not op.get_attr('transpose_a') and not op.get_attr('transpose_b'), (
      'Transpose on inputs not supported')

  inp_shape = context.shape_dict[x_name]
  out_shape = context.shape_dict[output_name]

  nB = inp_shape[-1]
  nC = out_shape[-1]
  W = np.transpose(W, (1, 0))

  bias = None
  has_bias = False

  #See if BiasAdd or Add can be fused
  for ops in context.all_ops:
    if ops.type == 'BiasAdd' or ops.type == 'Add':
      if compat.as_bytes(ops.inputs[0].name) == output_name:
        if compat.as_bytes(ops.inputs[1].name) in context.consts:
          bias = context.consts[compat.as_bytes(ops.inputs[1].name)]
          has_bias = True
        if (ops.inputs[1].op.type == 'Identity' and
            compat.as_bytes(ops.inputs[1].op.inputs[0].name) in context.consts):
          bias = context.consts[compat.as_bytes(
              ops.inputs[1].op.inputs[0].name)]
          has_bias = True
        if has_bias:
          BiasAdd_out_name = compat.as_bytes(ops.outputs[0].name)
          context.translated[BiasAdd_out_name] = True
          context.translated[output_name] = True
          output_name = BiasAdd_out_name
  context.builder.add_inner_product(op.name, # name
                                    W, # W
                                    bias, # Wb
                                    nB, # nB
                                    nC, # nC
                                    has_bias, # has_bias
                                    x_name, # input_name
                                    output_name # output_name
                                   )
  context.translated[output_name] = True

def _get_broadcasted_shape4(shapes):
  broadcasted_shape = [1, 1, 1, 1]
  for shape in shapes:
    rank = len(shape)
    shape4 = [1] * (4 - rank) + shape
    broadcasted_shape = [max(shape4[i], broadcasted_shape[i]) for i in \
        range(len(broadcasted_shape))]
  return broadcasted_shape

def _broadcast_axis(ref_shape4, shape):
  if None in shape: # when shape is not fully determined, just skip
    return None
  ref_shape = ref_shape4[-3:]
  rank = len(shape)
  shape = shape[-3:] if rank >= 3 else [1] * (3 - rank) + shape
  # shape and ref_shape are [H,W,C] now
  ratios = np.array(ref_shape) / np.array(shape)
  if ratios[0] != 1 or ratios[1] != 1:
    if ratios[0] != 1 and ratios[1] != 1:
      return None
    return 1 if ratios[0] != 1 else 2
  return None

def add(op, context):
  output_name = compat.as_bytes(op.outputs[0].name)

  # input_names: names of input tensors
  input_names = [make_tensor(ts, context) for ts in op.inputs]
  # input_shapes: shapes of input tensors
  input_shapes = [context.shape_dict[ts.name] for ts in op.inputs]
  mult_input_names = input_names

  # For rank-4 inputs, CoreML only allows [1], [C], [1,H,W] blobs to be
  # broadcasted in elementwise operations. To handle other broadcasting cases,
  # (e.g. [1,1,W] --> [C,H,W]), we insert up-sampling layers
  input_ranks = [len(shape) for shape in input_shapes]
  if 4 in input_ranks:
    broadcasted_shape4 = _get_broadcasted_shape4(input_shapes)
    for idx, in_name in enumerate(input_names):
      input_shape = input_shapes[idx]
      axis = _broadcast_axis(broadcasted_shape4, input_shape)
      if axis is not None:
        # add upsample layer
        upsampled_in_name = in_name + '__upsampled'
        mult_input_names[idx] = upsampled_in_name
        input_axis_dim = 1 if axis >= len(input_shape) else input_shape[axis]
        scale = broadcasted_shape4[axis] / input_axis_dim
        if axis == 1:
          context.builder.add_upsample(
              upsampled_in_name, scale, 1, in_name, upsampled_in_name)
        else:
          context.builder.add_upsample(
              upsampled_in_name, 1, scale, in_name, upsampled_in_name)

  context.builder.add_elementwise(
      output_name, mult_input_names, output_name, 'ADD')
  context.translated[output_name] = True

def mul(op, context):
  output_name = compat.as_bytes(op.outputs[0].name)

  # input_names: names of input tensors
  input_names = [make_tensor(ts, context) for ts in op.inputs]
  # input_shapes: shapes of input tensors
  input_shapes = [context.shape_dict[ts.name] for ts in op.inputs]
  mult_input_names = input_names

  # For rank-4 inputs, CoreML only allows [1], [C], [1,H,W] blobs to be
  # broadcasted in elementwise operations. To handle other broadcasting cases,
  # (e.g. [1,1,W] --> [C,H,W]), we insert up-sampling layers
  input_ranks = [len(shape) for shape in input_shapes]
  if 4 in input_ranks:
    broadcasted_shape4 = _get_broadcasted_shape4(input_shapes)
    for idx, in_name in enumerate(input_names):
      input_shape = input_shapes[idx]
      axis = _broadcast_axis(broadcasted_shape4, input_shape)
      if axis is not None:
        # add upsample layer
        upsampled_in_name = in_name + '__upsampled'
        mult_input_names[idx] = upsampled_in_name
        input_axis_dim = 1 if axis >= len(input_shape) else input_shape[axis]
        scale = broadcasted_shape4[axis] / input_axis_dim
        if axis == 1:
          context.builder.add_upsample(
              upsampled_in_name, scale, 1, in_name, upsampled_in_name)
        else:
          context.builder.add_upsample(
              upsampled_in_name, 1, scale, in_name, upsampled_in_name)

  context.builder.add_elementwise(
      output_name, mult_input_names, output_name, 'MULTIPLY')
  context.translated[output_name] = True

def neg(op, context):
  input_name = compat.as_bytes(op.inputs[0].name)
  output_name = compat.as_bytes(op.outputs[0].name)
  context.builder.add_activation(
      output_name, 'LINEAR', input_name, output_name, [-1.0, 0])
  context.translated[output_name] = True

def sub(op, context):
  assert len(op.inputs) == 2, 'Sub op currently supports only two inputs'
  output_name = compat.as_bytes(op.outputs[0].name)
  input_1_name = make_tensor(op.inputs[0], context)
  input_2_name = make_tensor(op.inputs[1], context)
  add_tensor_sub(
      context.builder, output_name, input_1_name, input_2_name, output_name)
  context.translated[output_name] = True

def rsqrt(op, context):
  input_name = compat.as_bytes(op.inputs[0].name)
  output_name = compat.as_bytes(op.outputs[0].name)
  context.builder.add_unary(output_name, input_name, output_name, 'rsqrt')
  context.translated[output_name] = True

def relu(op, context):
  input_name = compat.as_bytes(op.inputs[0].name)
  output_name = compat.as_bytes(op.outputs[0].name)
  context.builder.add_activation(output_name, 'RELU', input_name, output_name)
  context.translated[output_name] = True
  if op.type == 'QuantizedRelu':
    context.translated[op.outputs[1].name] = True
    context.translated[op.outputs[2].name] = True

def elu(op, context):
  input_name = compat.as_bytes(op.inputs[0].name)
  output_name = compat.as_bytes(op.outputs[0].name)
  context.builder.add_activation(output_name, 'ELU', input_name, output_name, 1.0)
  context.translated[output_name] = True
  
def tanh(op, context):
  input_name = compat.as_bytes(op.inputs[0].name)
  output_name = compat.as_bytes(op.outputs[0].name)
  context.builder.add_activation(output_name, 'TANH', input_name, output_name)
  context.translated[output_name] = True  

def relu6(op, context):
  input_name = compat.as_bytes(op.inputs[0].name)
  output_name = compat.as_bytes(op.outputs[0].name)

  relu_output_name = 'relu_' + output_name
  context.builder.add_activation(
      relu_output_name, 'RELU', input_name, relu_output_name)
  neg_output_name = relu_output_name + '_neg'
  # negate it
  context.builder.add_activation(
      neg_output_name, 'LINEAR', relu_output_name, neg_output_name, [-1.0, 0])
  # apply threshold
  clip_output_name = relu_output_name + '_clip'
  context.builder.add_unary(
      clip_output_name, neg_output_name, clip_output_name, 'threshold',
      alpha=-6.0)
  # negate it back
  context.builder.add_activation(
      output_name, 'LINEAR', clip_output_name, output_name, [-1.0, 0])
  context.translated[output_name] = True

def softmax(op, context):
  input_name = compat.as_bytes(op.inputs[0].name)
  output_name = compat.as_bytes(op.outputs[0].name)
  context.builder.add_softmax(output_name, input_name, output_name)
  context.translated[output_name] = True

def constant(op, context):
  assert compat.as_bytes(op.outputs[0].name) in context.consts, (
      'Value for {} not found'.format(op.outputs[0].name))

def greater(op, context):
  output_name = compat.as_bytes(op.outputs[0].name)
  assert len(op.inputs) == 2, 'Op Greater sees more than 2 inputs'
  assert len(op.inputs[1].shape) == 0, "Op Greater conversion can't handle non-constant"
  input_name = compat.as_bytes(op.inputs[0].name)
  const_name = compat.as_bytes(op.inputs[1].name)
  const_val = context.consts[const_name]
  alpha = 1000.0
  beta = 0.5 - alpha * const_val
  context.builder.add_activation(
      output_name, 'SIGMOID_HARD', input_name, output_name, params=[alpha, beta])
  context.translated[output_name] = True

def reduce_sum(op, context):
  ss_layers._add_reduce(op, context, 'sum')

def reduce_max(op, context):
  ss_layers._add_reduce(op, context, 'max')

def reduce_min(op, context):
  ss_layers._add_reduce(op, context, 'min')

def product(op, context):

  input_name = compat.as_bytes(op.inputs[0].name)
  output_name = compat.as_bytes(op.outputs[0].name)
  start_ind = context.consts[op.inputs[1].name]

  assert start_ind == 0, 'Prod: only start index = 0 case supported'

  input_shape = context.shape_dict[input_name]

  if len(input_shape) == 1:
    axis = 'C'
  else:
    assert False, 'Reduce Sum axis case not handled currently'

  mode = 'prod'
  context.translated[output_name] = True
  context.builder.add_reduce(output_name, input_name, output_name, axis, mode)

def mean(op, context):
  ss_layers._add_mean(op, context)

def mirror_pad(op, context):
  input_name = compat.as_bytes(op.inputs[0].name)
  output_name = compat.as_bytes(op.outputs[0].name)

  paddings = context.consts[op.inputs[1].name]
  top = paddings[1][0]
  bottom = paddings[1][1]
  left = paddings[2][0]
  right = paddings[2][1]

  assert op.get_attr('mode') != 'SYMMETRIC', \
      'symmetric mode is not supported by Core ML'

  context.translated[output_name] = True
  context.builder.add_padding(
      output_name, left, right, top, bottom,
      input_name=input_name, output_name=output_name,
      padding_type='reflection')

def pad(op, context):

  input_name = compat.as_bytes(op.inputs[0].name)
  output_name = compat.as_bytes(op.outputs[0].name)

  paddings = context.consts[op.inputs[1].name]
  top = paddings[1][0]
  bottom = paddings[1][1]
  left = paddings[2][0]
  right = paddings[2][1]
  channel_begin = paddings[3][0]
  channel_end = paddings[3][1]

  if channel_begin + channel_end == 0:
    context.builder.add_padding(
        output_name, left, right, top, bottom,
        input_name=input_name, output_name=output_name,
        padding_type='constant')
  elif top + bottom + left + right == 0:
    top = channel_begin
    bottom = channel_end
    context.builder.add_permute(
        output_name, (0, 2, 1, 3), input_name, output_name + 'swap_H_C')
    context.builder.add_padding(
        output_name, left, right, top, bottom,
        input_name=output_name + 'swap_H_C',
        output_name=output_name + 'padded_channel',
        padding_type='constant')
    context.builder.add_permute(
        output_name, (0, 2, 1, 3), output_name + 'padded_channel', output_name)
  else:
    assert False, 'Padding case not supported'

  context.translated[output_name] = True

def squared_difference(op, context):

  input_name = compat.as_bytes(op.inputs[0].name)
  input2 = compat.as_bytes(op.inputs[1].name)
  output_name = compat.as_bytes(op.outputs[0].name)

  context.translated[output_name] = True
  add_tensor_sub(
      context.builder, output_name + '_difference', input_name,
      input2, output_name + '_difference')
  context.builder.add_elementwise(
      output_name, [output_name + '_difference', output_name + '_difference'],
      output_name, 'MULTIPLY')

def square(op, context):

  input_name = compat.as_bytes(op.inputs[0].name)
  output_name = compat.as_bytes(op.outputs[0].name)

  context.translated[output_name] = True
  context.builder.add_elementwise(
      output_name, [input_name, input_name], output_name, 'MULTIPLY')

def resize_nearest_neighbor(op, context):

  input_name = compat.as_bytes(op.inputs[0].name)
  output_name = compat.as_bytes(op.outputs[0].name)

  if op.inputs[1].name in context.consts :
    output_spatial_sizes = context.consts[op.inputs[1].name]
  else:
    output_spatial_sizes = context.session.run(op.inputs[1].name,
                                feed_dict= context.input_feed_dict)

  shape = context.shape_dict[input_name]

  assert (len(shape) == 4), 'Resize Nearest Neighbour: unrecognized 4-D shape'
  assert (output_spatial_sizes[0] % shape[1] == 0), \
      'Resize Nearest Neighbour: height upsampling factor must be an integer'
  assert (output_spatial_sizes[1] % shape[2] == 0), \
      'Resize Nearest Neighbour: width upsampling factor must be an integer'

  upsample_factor_height = output_spatial_sizes[0]/shape[1]
  upsample_factor_width = output_spatial_sizes[1]/shape[2]

  context.builder.add_upsample(
      output_name, upsample_factor_height,
      upsample_factor_width, input_name, output_name, mode='NN')
  context.translated[output_name] = True

def sigmoid(op, context):
  input_name = compat.as_bytes(op.inputs[0].name)
  output_name = compat.as_bytes(op.outputs[0].name)

  context.translated[output_name] = True
  context.builder.add_activation(
      output_name, 'SIGMOID', input_name, output_name)

def transpose(op, context):
  assert len(op.inputs) == 2, 'Op Greater sees more than 2 inputs'
  output_name = compat.as_bytes(op.outputs[0].name)
  input_name = compat.as_bytes(op.inputs[0].name)
  param_name = compat.as_bytes(op.inputs[1].name)
  axes = list(context.consts[param_name])
  assert len(axes) == 4, "Op Transpose conversion only works with 4D tensors"

  # TODO - only works for 4D tensor without batch axis
  target_batch_idx = axes.index(0) # the assumed TF batch axis
  target_height_idx = axes.index(1) # the assumed TF height axis
  target_width_idx = axes.index(2) # the assumed TF width axis
  target_channel_idx = axes.index(3) # the assumed TF channel axis

  coreml_axes = [0]*4
  coreml_axes[target_batch_idx] = 0
  coreml_axes[target_height_idx] = 2
  coreml_axes[target_width_idx] = 3
  coreml_axes[target_channel_idx] = 1

  context.builder.add_permute(output_name, [], input_name, output_name)
  context.translated[output_name] = True

def real_div(op, context):
  output_name = compat.as_bytes(op.outputs[0].name)
  input_names = []
  for inp in op.inputs:
    input_names.append(make_tensor(inp, context))
  add_tensor_div(
      context.builder, output_name, input_names[0], input_names[1], output_name)
  context.translated[output_name] = True

def maximum(op, context):
  input_names = [compat.as_bytes(x.name) for x in op.inputs]
  output_name = compat.as_bytes(op.outputs[0].name)
  context.builder.add_elementwise(output_name, input_names, output_name, 'MAX')
  context.translated[output_name] = True

def shape(op, context):
  input_name = compat.as_bytes(op.inputs[0].name)
  output_name = compat.as_bytes(op.outputs[0].name)
  input_shape = context.shape_dict[input_name]
  if isinstance(input_shape, list):
    x = np.asarray(input_shape)
  else:
    x = np.asarray(list(input_shape))
  add_const(context, output_name, x, output_name, [len(input_shape), 1, 1])
  context.translated[output_name] = True

def random(op, context):
  # TODO - CoreML does not have random
  output_name = compat.as_bytes(op.outputs[0].name)
  output_shape = context.shape_dict[output_name]
  add_const(context, output_name, np.zeros((output_shape)), output_name)
  context.translated[output_name] = True

def argmax(op, context):
  input_name = compat.as_bytes(op.inputs[0].name)
  output_name = compat.as_bytes(op.outputs[0].name)

  input_shape = context.shape_dict[input_name]
  axis_tensor = compat.as_bytes(op.inputs[1].name)
  if axis_tensor in context.consts:
    axis_tf = context.consts[axis_tensor]
  else:
    assert False, 'ArgMax: Axis tensor not found in the list of Consts'
  if len(input_shape) == 4 and axis_tf == 3:
    axis = 'C'
  else:
    assert False, 'ArgMax: Axis translation case not handled currently'

  context.builder.add_reduce(
      output_name, input_name, output_name, axis, 'argmax')
  context.translated[output_name] = True

def extract_image_patches(op, context):
  # use a big convolution layer (that has weights!) for this op
  input_name = compat.as_bytes(op.inputs[0].name)
  output_name = compat.as_bytes(op.outputs[0].name)
  ksizes = op.get_attr('ksizes')
  padding_type = op.get_attr('padding')
  if padding_type == 'VALID':
    padding_type = 'valid'
  elif padding_type == 'SAME':
    padding_type = 'same'
  else:
    raise NotImplementedError('%s not implemented' %(padding_type))
  strides = op.get_attr('strides')
  rates = op.get_attr('rates')
  assert rates == [1] * len(rates), 'Only supports when rates are all 1s'
  kh, kw = ksizes[1], ksizes[2]
  sh, sw = strides[1], strides[2]

  c_in = context.shape_dict[input_name][-1]
  n_filters = kh * kw * c_in
  W = np.zeros((kh, kw, c_in, n_filters))
  for i_h in xrange(kh):
    for i_w in xrange(kw):
      for i_c in xrange(c_in):
        idx = i_c + (i_w * c_in) + (i_h * c_in * kw)
        W[i_h, i_w, i_c, idx] = 1

  context.builder.add_convolution(name=output_name,
                                  kernel_channels=c_in,
                                  output_channels=n_filters,
                                  height=kh,
                                  width=kw,
                                  stride_height=sh,
                                  stride_width=sw,
                                  border_mode=padding_type,
                                  groups=1,
                                  W=W,
                                  b=None,
                                  has_bias=False,
                                  is_deconv=False,
                                  output_shape=None,
                                  input_name=input_name,
                                  output_name=output_name)
  context.translated[output_name] = True

def one_hot(op, context):
  input_name = compat.as_bytes(op.inputs[0].name)
  output_name = compat.as_bytes(op.outputs[0].name)

  depth = context.consts[compat.as_bytes(op.inputs[1].name)]
  on_value = context.consts[compat.as_bytes(op.inputs[2].name)]
  off_value = context.consts[compat.as_bytes(op.inputs[3].name)]

  n_dims = depth
  W = np.ones((depth, depth)) * off_value
  for i in xrange(depth):
    W[i, i] = on_value
  context.builder.add_embedding(name=output_name,
                                W=W,
                                b=None,
                                input_dim=n_dims,
                                output_channels=n_dims,
                                has_bias=False,
                                input_name=input_name,
                                output_name=output_name)
  context.translated[output_name] = True

def fill(op, context):
  output_name = op.outputs[0].name

  assert op.inputs[1].name in context.consts, \
      'Second input to the Fill op must be a constant'
  assert output_name in context.shape_dict, \
      'Shape of the output of Fill must be known'
  shape = context.shape_dict[output_name]
  x = np.zeros(shape)
  add_const(context, output_name, x, output_name)
  context.translated[output_name] = True

def strided_slice(op, context):

  input_name = compat.as_bytes(op.inputs[0].name)
  output_name = compat.as_bytes(op.outputs[0].name)

  assert op.inputs[1].name in context.consts, \
      'Strided Slice: begin index must be a constant'
  assert op.inputs[2].name in context.consts, \
      'Strided Slice: end index must be a constant'
  assert op.inputs[3].name in context.consts, \
      'Strided Slice: strides must be a constant'

  begin = context.consts[compat.as_bytes(op.inputs[1].name)]
  end = context.consts[compat.as_bytes(op.inputs[2].name)]
  strides = context.consts[compat.as_bytes(op.inputs[3].name)]
  begin_mask = op.get_attr('begin_mask')
  end_mask = op.get_attr('end_mask')

  input_shape = context.shape_dict[input_name]

  if len(input_shape) == 1 and len(begin) == 1 and len(end) == 1 and \
      len(strides) == 1:
    if begin_mask:
      begin[0] = 0
    if end_mask:
      end[0] = input_shape[0]
    context.builder.add_slice(
        output_name, input_name, output_name,
        'channel', begin[0], end[0], strides[0])
  else:
    assert False, 'Strided Slice case not handled'
  context.translated[output_name] = True

def slice(op, context):

  input_name = compat.as_bytes(op.inputs[0].name)
  output_name = compat.as_bytes(op.outputs[0].name)

  assert op.inputs[1].name in context.consts, \
      'Slice: begin index must be a constant'
  assert op.inputs[2].name in context.consts, \
      'Slice: size must be a constant'

  begin = context.consts[compat.as_bytes(op.inputs[1].name)]
  size = context.consts[compat.as_bytes(op.inputs[2].name)]

  input_shape = context.shape_dict[input_name]
  if len(input_shape) == 1 and len(begin) == 1 and len(size) == 1:
    context.builder.add_slice(
        output_name, input_name, output_name,
        'channel', begin[0], begin[0] + size[0], 1)
  else:
    assert False, 'Slice case not handled'

  context.translated[output_name] = True


#just connect input names to output and record the mapping
def skip(op, context):
  #check if output is one of the network outputs
  # if it is then instead of skip, use an identity layer
  for out in op.outputs:
    if out.name in context.output_names:
      identity(op, context)
      return
  input_names = []
  for inp in op.inputs:
    input_names.append(inp.name)

  if len(input_names) > 1:
    del input_names[1:]

  assert len(input_names) == 1, (
      'Skip op must have only 1 input:' +
      ' This op of type %s cannot be skipped' % (op.type))
  inp_name = input_names[0]
  for out in op.outputs:
    if inp_name not in context.skip_map_names:
      context.skip_map_names[out.name] = inp_name
    else:
      context.skip_map_names[out.name] = context.skip_map_names[inp_name]
    context.translated[out.name] = True

#connect i-th output to the i-th input
def skip_one_to_one(op, context):
  for out in op.outputs:
    if out.name in context.output_names:
      identity(op, context)
      return

  assert len(op.inputs) == len(op.outputs), (
      'must have same number of outputs as inputs')

  for i, out in enumerate(op.outputs):
    inp_name = op.inputs[i].name
    if inp_name not in context.skip_map_names:
      context.skip_map_names[out.name] = inp_name
    else:
      context.skip_map_names[out.name] = context.skip_map_names[inp_name]
    context.translated[out.name] = True

#Only a very specific case of the gather op is handled
#Currently, CoreML cannot implement the general functionality of a gather op
def gather(op, context):

  output_name = op.outputs[0].name
  input_name = op.inputs[0].name

  assert len(context.shape_dict[op.inputs[0].name]) == 1, (
        'first input to \'gather\' must be a 1-D tensor')
  assert op.inputs[1].name in context.consts, (
         'second input to \'gather\' must be a constant')

  indices = context.consts[op.inputs[1].name]
  #check that indices are contiguous
  for i in range(len(indices)-1):
    if indices[i+1] - indices[i] != 1:
      raise ValueError('indices of the gather op must be contiguous')

  context.builder.add_slice(
    output_name, input_name, output_name,
    'channel', indices[0], indices[-1]+1, 1)

  context.translated[output_name] = True

def reciprocal(op, context):
  output_name = op.outputs[0].name
  input_name = op.inputs[0].name
  context.builder.add_unary(output_name, input_name, output_name, 'inverse')
  context.translated[output_name] = True

def lrn(op, context):
  input_name = compat.as_bytes(op.inputs[0].name)
  output_name = compat.as_bytes(op.outputs[0].name)

  input_shape = context.shape_dict[input_name]
  C = input_shape[-1]
  alpha = op.get_attr('alpha')
  beta = op.get_attr('beta')
  bias = op.get_attr('bias')
  depth_radius = op.get_attr('depth_radius')
  context.builder.add_lrn(output_name, input_name, output_name,
                          alpha=alpha * C,
                          beta=beta,
                          local_size=depth_radius,
                          k=bias)
  context.translated[output_name] = True
