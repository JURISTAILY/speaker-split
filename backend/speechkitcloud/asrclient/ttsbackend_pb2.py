# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ttsbackend.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import basic_pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='ttsbackend.proto',
  package='TTS',
  serialized_pb=_b('\n\x10ttsbackend.proto\x12\x03TTS\x1a\x0b\x62\x61sic.proto\"\x90\x04\n\x08Generate\x12\x11\n\tsessionId\x18\x1e \x01(\t\x12\x0c\n\x04lang\x18\x01 \x02(\t\x12\x0c\n\x04text\x18\x02 \x02(\t\x12\x10\n\x05speed\x18\x03 \x01(\x02:\x01\x31\x12+\n\x06voices\x18\x0b \x03(\x0b\x32\x1b.TTS.Generate.WeightedParam\x12-\n\x08\x65motions\x18\x0c \x03(\x0b\x32\x1b.TTS.Generate.WeightedParam\x12,\n\x07genders\x18\r \x03(\x0b\x32\x1b.TTS.Generate.WeightedParam\x12\x1e\n\x0frequireMetainfo\x18\x05 \x01(\x08:\x05\x66\x61lse\x12\x15\n\rmsd_threshold\x18\x0e \x01(\x02\x12\x16\n\x0emgc_recurrence\x18\x0f \x01(\x02\x12!\n\x19subtract_durations_sigmas\x18\x11 \x01(\x02\x12\x16\n\x0elf0_postfilter\x18\x12 \x01(\x02\x12\x13\n\x0bmgcGVWeight\x18\x13 \x01(\x02\x12\x13\n\x0blf0GVWeight\x18\x14 \x01(\x02\x12\x13\n\x0bmvfGVWeight\x18\x15 \x01(\x02\x12\x17\n\x0fmgc_postfilter1\x18\x16 \x01(\x02\x12\x17\n\x0fmgc_postfilter2\x18\x17 \x01(\x02\x12\x0f\n\x07\x63hunked\x18\x18 \x01(\x08\x1a-\n\rWeightedParam\x12\x0c\n\x04name\x18\x01 \x02(\t\x12\x0e\n\x06weight\x18\x02 \x02(\x02\"\xe5\x03\n\x10GenerateResponse\x12.\n\x05words\x18\x01 \x03(\x0b\x32\x1f.TTS.GenerateResponse.WordEvent\x12/\n\x08phonemes\x18\x02 \x03(\x0b\x32\x1d.TTS.GenerateResponse.Phoneme\x12\x11\n\taudioData\x18\x03 \x01(\x0c\x12\x11\n\tcompleted\x18\x04 \x02(\x08\x12\x44\n\x0cresponseCode\x18\x05 \x01(\x0e\x32..BasicProtobuf.ConnectionResponse.ResponseCode\x12\x0f\n\x07message\x18\x06 \x01(\t\x1a}\n\tWordEvent\x12\x1f\n\x17\x66irstCharPositionInText\x18\x01 \x02(\x05\x12\x1b\n\x13\x62ytesLengthInSignal\x18\x02 \x02(\x05\x12\x0c\n\x04text\x18\x03 \x01(\t\x12\x0e\n\x06postag\x18\x04 \x01(\t\x12\x14\n\x0chomographTag\x18\x05 \x01(\t\x1at\n\x07Phoneme\x12\x12\n\nttsPhoneme\x18\x01 \x02(\t\x12\x12\n\nIPAPhoneme\x18\x02 \x02(\t\x12\x0e\n\x06viseme\x18\x05 \x02(\x05\x12\x12\n\ndurationMs\x18\x03 \x02(\x05\x12\x1d\n\x15positionInBytesStream\x18\x04 \x02(\x05\"\x10\n\x0eStopGeneration')
  ,
  dependencies=[basic_pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_GENERATE_WEIGHTEDPARAM = _descriptor.Descriptor(
  name='WeightedParam',
  full_name='TTS.Generate.WeightedParam',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='TTS.Generate.WeightedParam.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='weight', full_name='TTS.Generate.WeightedParam.weight', index=1,
      number=2, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
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
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=522,
  serialized_end=567,
)

_GENERATE = _descriptor.Descriptor(
  name='Generate',
  full_name='TTS.Generate',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sessionId', full_name='TTS.Generate.sessionId', index=0,
      number=30, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='lang', full_name='TTS.Generate.lang', index=1,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='text', full_name='TTS.Generate.text', index=2,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='speed', full_name='TTS.Generate.speed', index=3,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='voices', full_name='TTS.Generate.voices', index=4,
      number=11, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='emotions', full_name='TTS.Generate.emotions', index=5,
      number=12, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='genders', full_name='TTS.Generate.genders', index=6,
      number=13, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='requireMetainfo', full_name='TTS.Generate.requireMetainfo', index=7,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='msd_threshold', full_name='TTS.Generate.msd_threshold', index=8,
      number=14, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='mgc_recurrence', full_name='TTS.Generate.mgc_recurrence', index=9,
      number=15, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='subtract_durations_sigmas', full_name='TTS.Generate.subtract_durations_sigmas', index=10,
      number=17, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='lf0_postfilter', full_name='TTS.Generate.lf0_postfilter', index=11,
      number=18, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='mgcGVWeight', full_name='TTS.Generate.mgcGVWeight', index=12,
      number=19, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='lf0GVWeight', full_name='TTS.Generate.lf0GVWeight', index=13,
      number=20, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='mvfGVWeight', full_name='TTS.Generate.mvfGVWeight', index=14,
      number=21, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='mgc_postfilter1', full_name='TTS.Generate.mgc_postfilter1', index=15,
      number=22, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='mgc_postfilter2', full_name='TTS.Generate.mgc_postfilter2', index=16,
      number=23, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='chunked', full_name='TTS.Generate.chunked', index=17,
      number=24, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_GENERATE_WEIGHTEDPARAM, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=39,
  serialized_end=567,
)


_GENERATERESPONSE_WORDEVENT = _descriptor.Descriptor(
  name='WordEvent',
  full_name='TTS.GenerateResponse.WordEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='firstCharPositionInText', full_name='TTS.GenerateResponse.WordEvent.firstCharPositionInText', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bytesLengthInSignal', full_name='TTS.GenerateResponse.WordEvent.bytesLengthInSignal', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='text', full_name='TTS.GenerateResponse.WordEvent.text', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='postag', full_name='TTS.GenerateResponse.WordEvent.postag', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='homographTag', full_name='TTS.GenerateResponse.WordEvent.homographTag', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=812,
  serialized_end=937,
)

_GENERATERESPONSE_PHONEME = _descriptor.Descriptor(
  name='Phoneme',
  full_name='TTS.GenerateResponse.Phoneme',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ttsPhoneme', full_name='TTS.GenerateResponse.Phoneme.ttsPhoneme', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='IPAPhoneme', full_name='TTS.GenerateResponse.Phoneme.IPAPhoneme', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='viseme', full_name='TTS.GenerateResponse.Phoneme.viseme', index=2,
      number=5, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='durationMs', full_name='TTS.GenerateResponse.Phoneme.durationMs', index=3,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='positionInBytesStream', full_name='TTS.GenerateResponse.Phoneme.positionInBytesStream', index=4,
      number=4, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
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
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=939,
  serialized_end=1055,
)

_GENERATERESPONSE = _descriptor.Descriptor(
  name='GenerateResponse',
  full_name='TTS.GenerateResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='words', full_name='TTS.GenerateResponse.words', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='phonemes', full_name='TTS.GenerateResponse.phonemes', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='audioData', full_name='TTS.GenerateResponse.audioData', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='completed', full_name='TTS.GenerateResponse.completed', index=3,
      number=4, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='responseCode', full_name='TTS.GenerateResponse.responseCode', index=4,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=200,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='message', full_name='TTS.GenerateResponse.message', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_GENERATERESPONSE_WORDEVENT, _GENERATERESPONSE_PHONEME, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=570,
  serialized_end=1055,
)


_STOPGENERATION = _descriptor.Descriptor(
  name='StopGeneration',
  full_name='TTS.StopGeneration',
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
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1057,
  serialized_end=1073,
)

_GENERATE_WEIGHTEDPARAM.containing_type = _GENERATE
_GENERATE.fields_by_name['voices'].message_type = _GENERATE_WEIGHTEDPARAM
_GENERATE.fields_by_name['emotions'].message_type = _GENERATE_WEIGHTEDPARAM
_GENERATE.fields_by_name['genders'].message_type = _GENERATE_WEIGHTEDPARAM
_GENERATERESPONSE_WORDEVENT.containing_type = _GENERATERESPONSE
_GENERATERESPONSE_PHONEME.containing_type = _GENERATERESPONSE
_GENERATERESPONSE.fields_by_name['words'].message_type = _GENERATERESPONSE_WORDEVENT
_GENERATERESPONSE.fields_by_name['phonemes'].message_type = _GENERATERESPONSE_PHONEME
_GENERATERESPONSE.fields_by_name['responseCode'].enum_type = basic_pb2._CONNECTIONRESPONSE_RESPONSECODE
DESCRIPTOR.message_types_by_name['Generate'] = _GENERATE
DESCRIPTOR.message_types_by_name['GenerateResponse'] = _GENERATERESPONSE
DESCRIPTOR.message_types_by_name['StopGeneration'] = _STOPGENERATION

Generate = _reflection.GeneratedProtocolMessageType('Generate', (_message.Message,), dict(

  WeightedParam = _reflection.GeneratedProtocolMessageType('WeightedParam', (_message.Message,), dict(
    DESCRIPTOR = _GENERATE_WEIGHTEDPARAM,
    __module__ = 'ttsbackend_pb2'
    # @@protoc_insertion_point(class_scope:TTS.Generate.WeightedParam)
    ))
  ,
  DESCRIPTOR = _GENERATE,
  __module__ = 'ttsbackend_pb2'
  # @@protoc_insertion_point(class_scope:TTS.Generate)
  ))
_sym_db.RegisterMessage(Generate)
_sym_db.RegisterMessage(Generate.WeightedParam)

GenerateResponse = _reflection.GeneratedProtocolMessageType('GenerateResponse', (_message.Message,), dict(

  WordEvent = _reflection.GeneratedProtocolMessageType('WordEvent', (_message.Message,), dict(
    DESCRIPTOR = _GENERATERESPONSE_WORDEVENT,
    __module__ = 'ttsbackend_pb2'
    # @@protoc_insertion_point(class_scope:TTS.GenerateResponse.WordEvent)
    ))
  ,

  Phoneme = _reflection.GeneratedProtocolMessageType('Phoneme', (_message.Message,), dict(
    DESCRIPTOR = _GENERATERESPONSE_PHONEME,
    __module__ = 'ttsbackend_pb2'
    # @@protoc_insertion_point(class_scope:TTS.GenerateResponse.Phoneme)
    ))
  ,
  DESCRIPTOR = _GENERATERESPONSE,
  __module__ = 'ttsbackend_pb2'
  # @@protoc_insertion_point(class_scope:TTS.GenerateResponse)
  ))
_sym_db.RegisterMessage(GenerateResponse)
_sym_db.RegisterMessage(GenerateResponse.WordEvent)
_sym_db.RegisterMessage(GenerateResponse.Phoneme)

StopGeneration = _reflection.GeneratedProtocolMessageType('StopGeneration', (_message.Message,), dict(
  DESCRIPTOR = _STOPGENERATION,
  __module__ = 'ttsbackend_pb2'
  # @@protoc_insertion_point(class_scope:TTS.StopGeneration)
  ))
_sym_db.RegisterMessage(StopGeneration)


# @@protoc_insertion_point(module_scope)
