
# def _init_db():

#     try:
#         db.metadata.create_all(db.engine)

#         db.session.add(Category(name='quantitative_timing', name_rus='Количественно-временные параметры'))
#         db.session.add(Category(name='speech_activity', name_rus='Параметры речевой активности'))
#         db.session.add(Category(name='semantic', name_rus='Лексико-семантический анализ'))
#         db.session.add(Category(name='emotional', name_rus='Анализ эмоционального состояния'))

#         db.session.flush()

#         default_category = db.session.query(Category).filter_by(name='speech_activity').one()

#         listed = [
#             ("Речь оператора, %",                            "operator_speech_ratio"),
#             ("Речь клиента, %",                              "client_speech_ratio"),
#             ("Речь оператора, сек",                          "operator_speech_duration"),
#             ("Речь клиента, сек",                            "client_speech_duration"),
#             ("Отношение речи оператора к речи клиента, %",   "operator_to_client_speech_ratio"),
#             ("Максимальный участок речи оператора, сек",     "operator_longest_speech_segment_duration"),
#             ("Максимальный участок речи клиента, сек",       "client_longest_speech_segment_duration"),

#             ("Перебивания, %",                            "both_interruptions_ratio"),
#             ("Перебивания, шт",                           "both_interruptions_count"),
#             ("Перебивания, сек",                          "both_interruptions_duration"),
#             ("Перебивания клиента оператором, %",         "operator_interruptions_ratio"),
#             ("Перебивания клиента оператором, шт",        "operator_interruptions_count"),
#             ("Перебивания клиента оператором, сек",       "operator_interruptions_duration"),
#             ("Перебивания оператора клиентом, %",         "client_interruptions_ratio"),
#             ("Перебивания оператора клиентом, шт",        "client_interruptions_count"),
#             ("Перебивания оператора клиентом, сек",       "client_interruptions_duration"),

#             ("Общая продолжительность молчания, %",                                        "both_silence_ratio"),
#             ("Общая продолжительность молчания, сек",                                      "both_silence_duration"),
#             ("Максимальный участок молчания, сек",                                         "both_longest_silence_segment_duration"),
#             ("Продолжительность молчания оператора, %",                                    "operator_silence_ratio"),
#             ("Продолжительность молчания оператора, сек",                                  "operator_silence_duration"),
#             ("Максимальный участок молчания оператора, сек",                               "operator_longest_silence_segment_duration"),
#             ("Продолжительность молчания клиента, %",                                      "client_silence_ratio"),
#             ("Продолжительность молчания клиента, сек",                                    "client_silence_duration"),
#             ("Максимальный участок молчания клиента,  сек",                                "client_longest_silence_segment_duration"),
#             ("Залипания оператора (паузы более 5-10 секунд после реплики клиента), сек",   "operator_freezing"),
#             ("Залипания клиента (паузы более 5-10 секунд после реплики оператора), сек",   "client_freezing"),
#         ]

#         for name_rus, name in listed:
#             db.session.add(ParameterMeta(name=name,
#                                          name_rus=name_rus,
#                                          category=default_category))

#         db.session.commit()

#     except Exception:
#         db.session.rollback()
#         raise


# def _add_call():
#     try:
#         call = Call(duration=12.4, is_incoming=True)

#         db.session.add(call)
#         db.session.flush()

#         values = [
#             ("operator_speech_ratio", 30.05),
#             ("client_speech_ratio", 40.66),
#             ("operator_speech_duration", 14.10),
#             ("client_speech_duration", 19.08),

#             ("operator_to_client_speech_ratio",  1.35),
#             ("client_longest_speech_segment_duration",  6.15),
#             ("operator_longest_speech_segment_duration",  4.53),


#             ("both_interruptions_ratio",  9.08),
#             ("both_interruptions_count",    13),
#             ("both_interruptions_duration",  0.09),

#             ("operator_interruptions_ratio",  3.01),
#             ("operator_interruptions_count",     7),
#             ("operator_interruptions_duration",  0.03),

#             ("client_interruptions_ratio",  5.88),
#             ("client_interruptions_count",     5),
#             ("client_interruptions_duration",  0.06),


#             ("both_silence_ratio", 38.36),
#             ("both_silence_duration", 18.00),
#             ("both_longest_silence_segment_duration",  5.22),

#             ("operator_silence_ratio", 59.34),
#             ("operator_silence_duration", 27.84),
#             ("operator_longest_silence_segment_duration",  4.74),

#             ("client_silence_ratio", 69.95),
#             ("client_silence_duration", 32.82),
#             ("client_longest_silence_segment_duration",  2.49),
#         ]

#         for name, value in values:
#             print(name, value)
#             meta = db.session.query(ParameterMeta).filter_by(name=name).one()
#             db.session.add(Parameter(call=call, parameter_meta_id=meta.id, value=value))

#         db.session.commit()

#     except Exception:
#         db.session.rollback()
#         raise
