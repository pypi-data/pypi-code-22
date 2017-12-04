# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: FeatureTypes.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='FeatureTypes.proto',
  package='CoreML.Specification',
  syntax='proto3',
  serialized_pb=_b('\n\x12\x46\x65\x61tureTypes.proto\x12\x14\x43oreML.Specification\"\x12\n\x10Int64FeatureType\"\x13\n\x11\x44oubleFeatureType\"\x13\n\x11StringFeatureType\"\xc0\x01\n\x10ImageFeatureType\x12\r\n\x05width\x18\x01 \x01(\x03\x12\x0e\n\x06height\x18\x02 \x01(\x03\x12\x45\n\ncolorSpace\x18\x03 \x01(\x0e\x32\x31.CoreML.Specification.ImageFeatureType.ColorSpace\"F\n\nColorSpace\x12\x17\n\x13INVALID_COLOR_SPACE\x10\x00\x12\r\n\tGRAYSCALE\x10\n\x12\x07\n\x03RGB\x10\x14\x12\x07\n\x03\x42GR\x10\x1e\"\xc1\x01\n\x10\x41rrayFeatureType\x12\r\n\x05shape\x18\x01 \x03(\x03\x12\x46\n\x08\x64\x61taType\x18\x02 \x01(\x0e\x32\x34.CoreML.Specification.ArrayFeatureType.ArrayDataType\"V\n\rArrayDataType\x12\x1b\n\x17INVALID_ARRAY_DATA_TYPE\x10\x00\x12\r\n\x07\x46LOAT32\x10\xa0\x80\x04\x12\x0c\n\x06\x44OUBLE\x10\xc0\x80\x04\x12\x0b\n\x05INT32\x10\xa0\x80\x08\"\xa4\x01\n\x15\x44ictionaryFeatureType\x12>\n\x0cint64KeyType\x18\x01 \x01(\x0b\x32&.CoreML.Specification.Int64FeatureTypeH\x00\x12@\n\rstringKeyType\x18\x02 \x01(\x0b\x32\'.CoreML.Specification.StringFeatureTypeH\x00\x42\t\n\x07KeyType\"\xab\x03\n\x0b\x46\x65\x61tureType\x12;\n\tint64Type\x18\x01 \x01(\x0b\x32&.CoreML.Specification.Int64FeatureTypeH\x00\x12=\n\ndoubleType\x18\x02 \x01(\x0b\x32\'.CoreML.Specification.DoubleFeatureTypeH\x00\x12=\n\nstringType\x18\x03 \x01(\x0b\x32\'.CoreML.Specification.StringFeatureTypeH\x00\x12;\n\timageType\x18\x04 \x01(\x0b\x32&.CoreML.Specification.ImageFeatureTypeH\x00\x12@\n\x0emultiArrayType\x18\x05 \x01(\x0b\x32&.CoreML.Specification.ArrayFeatureTypeH\x00\x12\x45\n\x0e\x64ictionaryType\x18\x06 \x01(\x0b\x32+.CoreML.Specification.DictionaryFeatureTypeH\x00\x12\x13\n\nisOptional\x18\xe8\x07 \x01(\x08\x42\x06\n\x04TypeB\x02H\x03\x62\x06proto3')
)



_IMAGEFEATURETYPE_COLORSPACE = _descriptor.EnumDescriptor(
  name='ColorSpace',
  full_name='CoreML.Specification.ImageFeatureType.ColorSpace',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='INVALID_COLOR_SPACE', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GRAYSCALE', index=1, number=10,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RGB', index=2, number=20,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BGR', index=3, number=30,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=229,
  serialized_end=299,
)
_sym_db.RegisterEnumDescriptor(_IMAGEFEATURETYPE_COLORSPACE)

_ARRAYFEATURETYPE_ARRAYDATATYPE = _descriptor.EnumDescriptor(
  name='ArrayDataType',
  full_name='CoreML.Specification.ArrayFeatureType.ArrayDataType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='INVALID_ARRAY_DATA_TYPE', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FLOAT32', index=1, number=65568,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DOUBLE', index=2, number=65600,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INT32', index=3, number=131104,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=409,
  serialized_end=495,
)
_sym_db.RegisterEnumDescriptor(_ARRAYFEATURETYPE_ARRAYDATATYPE)


_INT64FEATURETYPE = _descriptor.Descriptor(
  name='Int64FeatureType',
  full_name='CoreML.Specification.Int64FeatureType',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=44,
  serialized_end=62,
)


_DOUBLEFEATURETYPE = _descriptor.Descriptor(
  name='DoubleFeatureType',
  full_name='CoreML.Specification.DoubleFeatureType',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=64,
  serialized_end=83,
)


_STRINGFEATURETYPE = _descriptor.Descriptor(
  name='StringFeatureType',
  full_name='CoreML.Specification.StringFeatureType',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=85,
  serialized_end=104,
)


_IMAGEFEATURETYPE = _descriptor.Descriptor(
  name='ImageFeatureType',
  full_name='CoreML.Specification.ImageFeatureType',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='width', full_name='CoreML.Specification.ImageFeatureType.width', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='height', full_name='CoreML.Specification.ImageFeatureType.height', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='colorSpace', full_name='CoreML.Specification.ImageFeatureType.colorSpace', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _IMAGEFEATURETYPE_COLORSPACE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=107,
  serialized_end=299,
)


_ARRAYFEATURETYPE = _descriptor.Descriptor(
  name='ArrayFeatureType',
  full_name='CoreML.Specification.ArrayFeatureType',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='shape', full_name='CoreML.Specification.ArrayFeatureType.shape', index=0,
      number=1, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dataType', full_name='CoreML.Specification.ArrayFeatureType.dataType', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _ARRAYFEATURETYPE_ARRAYDATATYPE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=302,
  serialized_end=495,
)


_DICTIONARYFEATURETYPE = _descriptor.Descriptor(
  name='DictionaryFeatureType',
  full_name='CoreML.Specification.DictionaryFeatureType',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='int64KeyType', full_name='CoreML.Specification.DictionaryFeatureType.int64KeyType', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='stringKeyType', full_name='CoreML.Specification.DictionaryFeatureType.stringKeyType', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='KeyType', full_name='CoreML.Specification.DictionaryFeatureType.KeyType',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=498,
  serialized_end=662,
)


_FEATURETYPE = _descriptor.Descriptor(
  name='FeatureType',
  full_name='CoreML.Specification.FeatureType',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='int64Type', full_name='CoreML.Specification.FeatureType.int64Type', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='doubleType', full_name='CoreML.Specification.FeatureType.doubleType', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='stringType', full_name='CoreML.Specification.FeatureType.stringType', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='imageType', full_name='CoreML.Specification.FeatureType.imageType', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='multiArrayType', full_name='CoreML.Specification.FeatureType.multiArrayType', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dictionaryType', full_name='CoreML.Specification.FeatureType.dictionaryType', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='isOptional', full_name='CoreML.Specification.FeatureType.isOptional', index=6,
      number=1000, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='Type', full_name='CoreML.Specification.FeatureType.Type',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=665,
  serialized_end=1092,
)

_IMAGEFEATURETYPE.fields_by_name['colorSpace'].enum_type = _IMAGEFEATURETYPE_COLORSPACE
_IMAGEFEATURETYPE_COLORSPACE.containing_type = _IMAGEFEATURETYPE
_ARRAYFEATURETYPE.fields_by_name['dataType'].enum_type = _ARRAYFEATURETYPE_ARRAYDATATYPE
_ARRAYFEATURETYPE_ARRAYDATATYPE.containing_type = _ARRAYFEATURETYPE
_DICTIONARYFEATURETYPE.fields_by_name['int64KeyType'].message_type = _INT64FEATURETYPE
_DICTIONARYFEATURETYPE.fields_by_name['stringKeyType'].message_type = _STRINGFEATURETYPE
_DICTIONARYFEATURETYPE.oneofs_by_name['KeyType'].fields.append(
  _DICTIONARYFEATURETYPE.fields_by_name['int64KeyType'])
_DICTIONARYFEATURETYPE.fields_by_name['int64KeyType'].containing_oneof = _DICTIONARYFEATURETYPE.oneofs_by_name['KeyType']
_DICTIONARYFEATURETYPE.oneofs_by_name['KeyType'].fields.append(
  _DICTIONARYFEATURETYPE.fields_by_name['stringKeyType'])
_DICTIONARYFEATURETYPE.fields_by_name['stringKeyType'].containing_oneof = _DICTIONARYFEATURETYPE.oneofs_by_name['KeyType']
_FEATURETYPE.fields_by_name['int64Type'].message_type = _INT64FEATURETYPE
_FEATURETYPE.fields_by_name['doubleType'].message_type = _DOUBLEFEATURETYPE
_FEATURETYPE.fields_by_name['stringType'].message_type = _STRINGFEATURETYPE
_FEATURETYPE.fields_by_name['imageType'].message_type = _IMAGEFEATURETYPE
_FEATURETYPE.fields_by_name['multiArrayType'].message_type = _ARRAYFEATURETYPE
_FEATURETYPE.fields_by_name['dictionaryType'].message_type = _DICTIONARYFEATURETYPE
_FEATURETYPE.oneofs_by_name['Type'].fields.append(
  _FEATURETYPE.fields_by_name['int64Type'])
_FEATURETYPE.fields_by_name['int64Type'].containing_oneof = _FEATURETYPE.oneofs_by_name['Type']
_FEATURETYPE.oneofs_by_name['Type'].fields.append(
  _FEATURETYPE.fields_by_name['doubleType'])
_FEATURETYPE.fields_by_name['doubleType'].containing_oneof = _FEATURETYPE.oneofs_by_name['Type']
_FEATURETYPE.oneofs_by_name['Type'].fields.append(
  _FEATURETYPE.fields_by_name['stringType'])
_FEATURETYPE.fields_by_name['stringType'].containing_oneof = _FEATURETYPE.oneofs_by_name['Type']
_FEATURETYPE.oneofs_by_name['Type'].fields.append(
  _FEATURETYPE.fields_by_name['imageType'])
_FEATURETYPE.fields_by_name['imageType'].containing_oneof = _FEATURETYPE.oneofs_by_name['Type']
_FEATURETYPE.oneofs_by_name['Type'].fields.append(
  _FEATURETYPE.fields_by_name['multiArrayType'])
_FEATURETYPE.fields_by_name['multiArrayType'].containing_oneof = _FEATURETYPE.oneofs_by_name['Type']
_FEATURETYPE.oneofs_by_name['Type'].fields.append(
  _FEATURETYPE.fields_by_name['dictionaryType'])
_FEATURETYPE.fields_by_name['dictionaryType'].containing_oneof = _FEATURETYPE.oneofs_by_name['Type']
DESCRIPTOR.message_types_by_name['Int64FeatureType'] = _INT64FEATURETYPE
DESCRIPTOR.message_types_by_name['DoubleFeatureType'] = _DOUBLEFEATURETYPE
DESCRIPTOR.message_types_by_name['StringFeatureType'] = _STRINGFEATURETYPE
DESCRIPTOR.message_types_by_name['ImageFeatureType'] = _IMAGEFEATURETYPE
DESCRIPTOR.message_types_by_name['ArrayFeatureType'] = _ARRAYFEATURETYPE
DESCRIPTOR.message_types_by_name['DictionaryFeatureType'] = _DICTIONARYFEATURETYPE
DESCRIPTOR.message_types_by_name['FeatureType'] = _FEATURETYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Int64FeatureType = _reflection.GeneratedProtocolMessageType('Int64FeatureType', (_message.Message,), dict(
  DESCRIPTOR = _INT64FEATURETYPE,
  __module__ = 'FeatureTypes_pb2'
  # @@protoc_insertion_point(class_scope:CoreML.Specification.Int64FeatureType)
  ))
_sym_db.RegisterMessage(Int64FeatureType)

DoubleFeatureType = _reflection.GeneratedProtocolMessageType('DoubleFeatureType', (_message.Message,), dict(
  DESCRIPTOR = _DOUBLEFEATURETYPE,
  __module__ = 'FeatureTypes_pb2'
  # @@protoc_insertion_point(class_scope:CoreML.Specification.DoubleFeatureType)
  ))
_sym_db.RegisterMessage(DoubleFeatureType)

StringFeatureType = _reflection.GeneratedProtocolMessageType('StringFeatureType', (_message.Message,), dict(
  DESCRIPTOR = _STRINGFEATURETYPE,
  __module__ = 'FeatureTypes_pb2'
  # @@protoc_insertion_point(class_scope:CoreML.Specification.StringFeatureType)
  ))
_sym_db.RegisterMessage(StringFeatureType)

ImageFeatureType = _reflection.GeneratedProtocolMessageType('ImageFeatureType', (_message.Message,), dict(
  DESCRIPTOR = _IMAGEFEATURETYPE,
  __module__ = 'FeatureTypes_pb2'
  # @@protoc_insertion_point(class_scope:CoreML.Specification.ImageFeatureType)
  ))
_sym_db.RegisterMessage(ImageFeatureType)

ArrayFeatureType = _reflection.GeneratedProtocolMessageType('ArrayFeatureType', (_message.Message,), dict(
  DESCRIPTOR = _ARRAYFEATURETYPE,
  __module__ = 'FeatureTypes_pb2'
  # @@protoc_insertion_point(class_scope:CoreML.Specification.ArrayFeatureType)
  ))
_sym_db.RegisterMessage(ArrayFeatureType)

DictionaryFeatureType = _reflection.GeneratedProtocolMessageType('DictionaryFeatureType', (_message.Message,), dict(
  DESCRIPTOR = _DICTIONARYFEATURETYPE,
  __module__ = 'FeatureTypes_pb2'
  # @@protoc_insertion_point(class_scope:CoreML.Specification.DictionaryFeatureType)
  ))
_sym_db.RegisterMessage(DictionaryFeatureType)

FeatureType = _reflection.GeneratedProtocolMessageType('FeatureType', (_message.Message,), dict(
  DESCRIPTOR = _FEATURETYPE,
  __module__ = 'FeatureTypes_pb2'
  # @@protoc_insertion_point(class_scope:CoreML.Specification.FeatureType)
  ))
_sym_db.RegisterMessage(FeatureType)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('H\003'))
# @@protoc_insertion_point(module_scope)
