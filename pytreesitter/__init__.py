import os.path as path
import platform

from ctypes import c_void_p
from ctypes import cdll
from ctypes.util import find_library
from distutils.ccompiler import new_compiler
from tempfile import TemporaryDirectory

from pytreesitter._binding import *


class Language:
    def build_library(output_path, repo_paths):
        """
        Build a dynamic library at the given path, based on the parser
        repositories at the given paths.

        Returns `True` if the dynamic library was compiled and `False` if
        the library already existed and was modified more recently than
        any of the source files.
        """
        output_mtime = 0
        if path.exists(output_path):
            output_mtime = path.getmtime(output_path)

        if len(repo_paths) == 0:
            raise ValueError('Must provide at least one language folder')

        cpp = False
        source_paths = []
        source_mtimes = [path.getmtime(__file__)]
        for repo_path in repo_paths:
            src_path = path.join(repo_path, 'src')
            source_paths.append(path.join(src_path, "parser.c"))
            source_mtimes.append(path.getmtime(source_paths[-1]))
            if path.exists(path.join(src_path, "scanner.cc")):
                cpp = True
                source_paths.append(path.join(src_path, "scanner.cc"))
                source_mtimes.append(path.getmtime(source_paths[-1]))
            elif path.exists(path.join(src_path, "scanner.c")):
                source_paths.append(path.join(src_path, "scanner.c"))
                source_mtimes.append(path.getmtime(source_paths[-1]))

        compiler = new_compiler()
        if cpp:
            if find_library('c++'):
                compiler.add_library('c++')
            elif find_library('stdc++'):
                compiler.add_library('stdc++')

        if max(source_mtimes) > output_mtime:
            with TemporaryDirectory(suffix='tree_sitter_language') as dir:
                object_paths = []
                for source_path in source_paths:
                    if platform.system() == 'Windows':
                        flags = None
                    else:
                        flags = ['-fPIC']
                        if source_path.endswith('.c'):
                            flags.append('-std=c99')
                    object_paths.append(compiler.compile(
                        [source_path],
                        output_dir=dir,
                        include_dirs=[path.dirname(source_path)],
                        extra_preargs=flags
                    )[0])
                compiler.link_shared_object(object_paths, output_path)
            return True
        else:
            return False

    def __init__(self, library_path, name):
        """
        Load the language with the given name from the dynamic library
        at the given path.
        """
        self.name = name
        self.lib = cdll.LoadLibrary(library_path)
        language_function = getattr(self.lib, "tree_sitter_%s" % name)
        language_function.restype = c_void_p
        self.language_id = language_function()


# __all__ = [
#     "Language",

#     "delete_TSFieldMapEntry",
#     "delete_TSFieldMapSlice",
#     "delete_TSInput",
#     "delete_TSInputEdit",
#     "delete_TSLanguage",
#     "delete_TSLanguage_external_scanner",
#     "delete_TSLexer",
#     "delete_TSLexMode",
#     "delete_TSLogger",
#     "delete_TSNode",
#     "delete_TSParseAction",
#     "delete_TSParseAction_params",
#     "delete_TSParseActionEntry",
#     "delete_TSPoint",
#     "delete_TSRange",
#     "delete_TSSymbolMetadata",
#     "delete_TSTreeCursor",
#     "new_TSFieldMapEntry",
#     "new_TSFieldMapSlice",
#     "new_TSInput",
#     "new_TSInputEdit",
#     "new_TSLanguage",
#     "new_TSLanguage_external_scanner",
#     "new_TSLexer",
#     "new_TSLexMode",
#     "new_TSLogger",
#     "new_TSNode",
#     "new_TSParseAction",
#     "new_TSParseAction_params",
#     "new_TSParseActionEntry",
#     "new_TSPoint",
#     "new_TSRange",
#     "new_TSSymbolMetadata",
#     "new_TSTreeCursor",
#     "TREE_SITTER_LANGUAGE_VERSION",
#     "TREE_SITTER_MIN_COMPATIBLE_LANGUAGE_VERSION",
#     "TREE_SITTER_SERIALIZATION_BUFFER_SIZE",
#     "ts_builtin_sym_end",
#     "ts_language_field_count",
#     "ts_language_field_id_for_name",
#     "ts_language_field_name_for_id",
#     "ts_language_symbol_count",
#     "ts_language_symbol_for_name",
#     "ts_language_symbol_name",
#     "ts_language_symbol_type",
#     "ts_language_version",
#     "ts_node_child",
#     "ts_node_child_by_field_id",
#     "ts_node_child_by_field_name",
#     "ts_node_child_count",
#     "ts_node_descendant_for_byte_range",
#     "ts_node_descendant_for_point_range",
#     "ts_node_edit",
#     "ts_node_end_byte",
#     "ts_node_end_point",
#     "ts_node_eq",
#     "ts_node_first_child_for_byte",
#     "ts_node_first_named_child_for_byte",
#     "ts_node_has_changes",
#     "ts_node_has_error",
#     "ts_node_is_missing",
#     "ts_node_is_named",
#     "ts_node_is_null",
#     "ts_node_named_child",
#     "ts_node_named_child_count",
#     "ts_node_named_descendant_for_byte_range",
#     "ts_node_named_descendant_for_point_range",
#     "ts_node_next_named_sibling",
#     "ts_node_next_sibling",
#     "ts_node_parent",
#     "ts_node_prev_named_sibling",
#     "ts_node_prev_sibling",
#     "ts_node_start_byte",
#     "ts_node_start_point",
#     "ts_node_string",
#     "ts_node_symbol",
#     "ts_node_type",
#     "ts_parser_cancellation_flag",
#     "ts_parser_delete",
#     "ts_parser_halt_on_error",
#     "ts_parser_included_ranges",
#     "ts_parser_language",
#     "ts_parser_logger",
#     "ts_parser_new",
#     "ts_parser_parse",
#     "ts_parser_parse_string",
#     "ts_parser_parse_string_encoding",
#     "ts_parser_print_dot_graphs",
#     "ts_parser_reset",
#     "ts_parser_set_cancellation_flag",
#     "ts_parser_set_included_ranges",
#     "ts_parser_set_language",
#     "ts_parser_set_logger",
#     "ts_parser_set_timeout_micros",
#     "ts_parser_timeout_micros",
#     "ts_tree_copy",
#     "ts_tree_cursor_current_field_id",
#     "ts_tree_cursor_current_field_name",
#     "ts_tree_cursor_current_node",
#     "ts_tree_cursor_delete",
#     "ts_tree_cursor_goto_first_child",
#     "ts_tree_cursor_goto_first_child_for_byte",
#     "ts_tree_cursor_goto_next_sibling",
#     "ts_tree_cursor_goto_parent",
#     "ts_tree_cursor_new",
#     "ts_tree_cursor_reset",
#     "ts_tree_delete",
#     "ts_tree_edit",
#     "ts_tree_get_changed_ranges",
#     "ts_tree_language",
#     "ts_tree_print_dot_graph",
#     "ts_tree_root_node",
#     "TSFieldMapEntry_child_index_get",
#     "TSFieldMapEntry_child_index_set",
#     "TSFieldMapEntry_field_id_get",
#     "TSFieldMapEntry_field_id_set",
#     "TSFieldMapEntry_inherited_get",
#     "TSFieldMapEntry_inherited_set",
#     "TSFieldMapSlice_index_get",
#     "TSFieldMapSlice_index_set",
#     "TSFieldMapSlice_length_get",
#     "TSFieldMapSlice_length_set",
#     "TSInput_encoding_get",
#     "TSInput_encoding_set",
#     "TSInput_payload_get",
#     "TSInput_payload_set",
#     "TSInput_read_get",
#     "TSInput_read_set",
#     "TSInputEdit_new_end_byte_get",
#     "TSInputEdit_new_end_byte_set",
#     "TSInputEdit_new_end_point_get",
#     "TSInputEdit_new_end_point_set",
#     "TSInputEdit_old_end_byte_get",
#     "TSInputEdit_old_end_byte_set",
#     "TSInputEdit_old_end_point_get",
#     "TSInputEdit_old_end_point_set",
#     "TSInputEdit_start_byte_get",
#     "TSInputEdit_start_byte_set",
#     "TSInputEdit_start_point_get",
#     "TSInputEdit_start_point_set",
#     "TSInputEncodingUTF16",
#     "TSInputEncodingUTF8",
#     "TSLanguage_alias_count_get",
#     "TSLanguage_alias_count_set",
#     "TSLanguage_alias_sequences_get",
#     "TSLanguage_alias_sequences_set",
#     "TSLanguage_external_scanner_create_get",
#     "TSLanguage_external_scanner_create_set",
#     "TSLanguage_external_scanner_deserialize_get",
#     "TSLanguage_external_scanner_deserialize_set",
#     "TSLanguage_external_scanner_destroy_get",
#     "TSLanguage_external_scanner_destroy_set",
#     "TSLanguage_external_scanner_get",
#     "TSLanguage_external_scanner_scan_get",
#     "TSLanguage_external_scanner_scan_set",
#     "TSLanguage_external_scanner_serialize_get",
#     "TSLanguage_external_scanner_serialize_set",
#     "TSLanguage_external_scanner_states_get",
#     "TSLanguage_external_scanner_states_set",
#     "TSLanguage_external_scanner_symbol_map_get",
#     "TSLanguage_external_scanner_symbol_map_set",
#     "TSLanguage_external_token_count_get",
#     "TSLanguage_external_token_count_set",
#     "TSLanguage_field_count_get",
#     "TSLanguage_field_count_set",
#     "TSLanguage_field_map_entries_get",
#     "TSLanguage_field_map_entries_set",
#     "TSLanguage_field_map_slices_get",
#     "TSLanguage_field_map_slices_set",
#     "TSLanguage_field_names_get",
#     "TSLanguage_field_names_set",
#     "TSLanguage_keyword_capture_token_get",
#     "TSLanguage_keyword_capture_token_set",
#     "TSLanguage_keyword_lex_fn_get",
#     "TSLanguage_keyword_lex_fn_set",
#     "TSLanguage_lex_fn_get",
#     "TSLanguage_lex_fn_set",
#     "TSLanguage_lex_modes_get",
#     "TSLanguage_lex_modes_set",
#     "TSLanguage_max_alias_sequence_length_get",
#     "TSLanguage_max_alias_sequence_length_set",
#     "TSLanguage_parse_actions_get",
#     "TSLanguage_parse_actions_set",
#     "TSLanguage_parse_table_get",
#     "TSLanguage_parse_table_set",
#     "TSLanguage_symbol_count_get",
#     "TSLanguage_symbol_count_set",
#     "TSLanguage_symbol_metadata_get",
#     "TSLanguage_symbol_metadata_set",
#     "TSLanguage_symbol_names_get",
#     "TSLanguage_symbol_names_set",
#     "TSLanguage_token_count_get",
#     "TSLanguage_token_count_set",
#     "TSLanguage_version_get",
#     "TSLanguage_version_set",
#     "TSLexer_advance_get",
#     "TSLexer_advance_set",
#     "TSLexer_get_column_get",
#     "TSLexer_get_column_set",
#     "TSLexer_is_at_included_range_start_get",
#     "TSLexer_is_at_included_range_start_set",
#     "TSLexer_lookahead_get",
#     "TSLexer_lookahead_set",
#     "TSLexer_mark_end_get",
#     "TSLexer_mark_end_set",
#     "TSLexer_result_symbol_get",
#     "TSLexer_result_symbol_set",
#     "TSLexMode_external_lex_state_get",
#     "TSLexMode_external_lex_state_set",
#     "TSLexMode_lex_state_get",
#     "TSLexMode_lex_state_set",
#     "TSLogger_log_get",
#     "TSLogger_log_set",
#     "TSLogger_payload_get",
#     "TSLogger_payload_set",
#     "TSLogTypeLex",
#     "TSLogTypeParse",
#     "TSNode_context_get",
#     "TSNode_context_set",
#     "TSNode_id_get",
#     "TSNode_id_set",
#     "TSNode_tree_get",
#     "TSNode_tree_set",
#     "TSParseAction_params_child_count_get",
#     "TSParseAction_params_child_count_set",
#     "TSParseAction_params_dynamic_precedence_get",
#     "TSParseAction_params_dynamic_precedence_set",
#     "TSParseAction_params_extra_get",
#     "TSParseAction_params_extra_set",
#     "TSParseAction_params_get",
#     "TSParseAction_params_production_id_get",
#     "TSParseAction_params_production_id_set",
#     "TSParseAction_params_repetition_get",
#     "TSParseAction_params_repetition_set",
#     "TSParseAction_params_state_get",
#     "TSParseAction_params_state_set",
#     "TSParseAction_params_symbol_get",
#     "TSParseAction_params_symbol_set",
#     "TSParseAction_type_get",
#     "TSParseAction_type_set",
#     "TSParseActionEntry_action_get",
#     "TSParseActionEntry_action_set",
#     "TSParseActionEntry_count_get",
#     "TSParseActionEntry_count_set",
#     "TSParseActionEntry_reusable_get",
#     "TSParseActionEntry_reusable_set",
#     "TSParseActionTypeAccept",
#     "TSParseActionTypeRecover",
#     "TSParseActionTypeReduce",
#     "TSParseActionTypeShift",
#     "TSPoint_column_get",
#     "TSPoint_column_set",
#     "TSPoint_row_get",
#     "TSPoint_row_set",
#     "TSRange_end_byte_get",
#     "TSRange_end_byte_set",
#     "TSRange_end_point_get",
#     "TSRange_end_point_set",
#     "TSRange_start_byte_get",
#     "TSRange_start_byte_set",
#     "TSRange_start_point_get",
#     "TSRange_start_point_set",
#     "TSSymbolMetadata_named_get",
#     "TSSymbolMetadata_named_set",
#     "TSSymbolMetadata_visible_get",
#     "TSSymbolMetadata_visible_set",
#     "TSSymbolTypeAnonymous",
#     "TSSymbolTypeAuxiliary",
#     "TSSymbolTypeRegular",
#     "TSTreeCursor_context_get",
#     "TSTreeCursor_context_set",
#     "TSTreeCursor_id_get",
#     "TSTreeCursor_id_set",
#     "TSTreeCursor_tree_get",
#     "TSTreeCursor_tree_set",
# ]
