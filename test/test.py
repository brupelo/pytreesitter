from pytreesitter import *
import sys


if __name__ == '__main__':
    # print(TREE_SITTER_LANGUAGE_VERSION)
    # print(TREE_SITTER_MIN_COMPATIBLE_LANGUAGE_VERSION)
    # print(TREE_SITTER_SERIALIZATION_BUFFER_SIZE)
    # print('-' * 80)
    # print(dir())

    parser = ts_parser_new()

    # Note: You need to copy your own shared library here, not uploading binaries to the repo :P
    PY_LANGUAGE = Language("bin/python/python.pyd", "python")

    # Question: I've got stuck at this point, how can I cast to TSLanguage over here?
    # lang = new_TSLanguage(PY_LANGUAGE.language_id)  # <--- Not working
