import tempfile


def gen_temp_file(name=''):
    return tempfile.NamedTemporaryFile(prefix='{}_'.format(name),
                                       suffix='.wav',
                                       delete=False)
