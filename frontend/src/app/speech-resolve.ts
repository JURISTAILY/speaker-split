export const PARAMS_KEY_RESOLVE = function(name : string) : string {
  const PARAMS_NAME_MAP = {
    emotional : 'Эмоциональное состояние',
    quantitative_timing  : 'Количественно-временные параметры',
    operator_speech_ratio : 'Речь оператора, %',
    operator_speech_duration : 'Речь оператора, сек',
    operator_interruptions : 'Оператор перебивает клиента, шт',
    semantic : 'Лексико-семантический анализ',
    speech_activity : 'Параметры речевой активности'
  };

  if (name in PARAMS_NAME_MAP) {
    return PARAMS_NAME_MAP[name];
  }
  return name;
}