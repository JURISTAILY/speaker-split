# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: basic.proto

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
  name='basic.proto',
  package='BasicProtobuf',
  syntax='proto2',
  serialized_pb=_b('\n\x0b\x62\x61sic.proto\x12\rBasicProtobuf\"\xc4\x02\n\x12\x43onnectionResponse\x12\x44\n\x0cresponseCode\x18\x01 \x02(\x0e\x32..BasicProtobuf.ConnectionResponse.ResponseCode\x12\x11\n\tsessionId\x18\x02 \x02(\t\x12\x0f\n\x07message\x18\x03 \x01(\t\"\xc3\x01\n\x0cResponseCode\x12\x07\n\x02OK\x10\xc8\x01\x12\x19\n\x14\x42\x61\x64MessageFormatting\x10\x90\x03\x12\x13\n\x0eUnknownService\x10\x94\x03\x12\x18\n\x13NotSupportedVersion\x10\x95\x03\x12\x0c\n\x07Timeout\x10\x98\x03\x12\x12\n\rProtocolError\x10\x9a\x03\x12\x12\n\rInternalError\x10\xf4\x03\x12\x0f\n\nInvalidKey\x10\xad\x03\x12\x19\n\x14InvalidRequestParams\x10\x96\x03')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_CONNECTIONRESPONSE_RESPONSECODE = _descriptor.EnumDescriptor(
  name='ResponseCode',
  full_name='BasicProtobuf.ConnectionResponse.ResponseCode',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='OK', index=0, number=200,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BadMessageFormatting', index=1, number=400,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UnknownService', index=2, number=404,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NotSupportedVersion', index=3, number=405,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='Timeout', index=4, number=408,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ProtocolError', index=5, number=410,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='InternalError', index=6, number=500,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='InvalidKey', index=7, number=429,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='InvalidRequestParams', index=8, number=406,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=160,
  serialized_end=355,
)
_sym_db.RegisterEnumDescriptor(_CONNECTIONRESPONSE_RESPONSECODE)


_CONNECTIONRESPONSE = _descriptor.Descriptor(
  name='ConnectionResponse',
  full_name='BasicProtobuf.ConnectionResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='responseCode', full_name='BasicProtobuf.ConnectionResponse.responseCode', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=200,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sessionId', full_name='BasicProtobuf.ConnectionResponse.sessionId', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='message', full_name='BasicProtobuf.ConnectionResponse.message', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _CONNECTIONRESPONSE_RESPONSECODE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=31,
  serialized_end=355,
)

_CONNECTIONRESPONSE.fields_by_name['responseCode'].enum_type = _CONNECTIONRESPONSE_RESPONSECODE
_CONNECTIONRESPONSE_RESPONSECODE.containing_type = _CONNECTIONRESPONSE
DESCRIPTOR.message_types_by_name['ConnectionResponse'] = _CONNECTIONRESPONSE

ConnectionResponse = _reflection.GeneratedProtocolMessageType('ConnectionResponse', (_message.Message,), dict(
  DESCRIPTOR = _CONNECTIONRESPONSE,
  __module__ = 'basic_pb2'
  # @@protoc_insertion_point(class_scope:BasicProtobuf.ConnectionResponse)
  ))
_sym_db.RegisterMessage(ConnectionResponse)


# @@protoc_insertion_point(module_scope)
