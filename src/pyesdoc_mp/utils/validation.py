"""A set of CIM meta-programming ontology configurqtion validation functions.

"""
# Module level imports.
import os
import re


# Set of supported programming languages.
_LANGUAGES = [
    'c++',
    'fortran',
    'java',
    'javascript',
    'python',
]


def _get_schema():
    """Returns configuration schema.

    """
    return {
        'ontology' : {
            'type' : dict,
            'fields' : {
                'name' : (str, True, '^[a-z_]+$'),
                'version' : (str, True, '^[0-9\.]+$'),
                'doc' : (str, True, None),
                'packages' : ('packages', True, None),
            },
        },
        'packages': {
            'type' : list,
            'item_type' : 'package',
        },
        'package' : {
            'type' : dict,
            'fields' : {
                'name' : (str, True, '^[a-z]+$'),
                'doc' : (str, True, None),
                'classes' : ('classes', True, None),
                'enums' : ('enums', True, None),
            },
        },
        'classes': {
            'type' : list,
            'item_type' : 'class',
        },
        'class' : {
            'type' : dict,
            'fields' : {
                'name' : (str, True, '^[a-z_0-9]+$'),
                'base' : (str, False, '^[a-z_]+\.?[a-z_]+$'),
                'abstract' : (bool, True, None),
                'doc' : (str, False, None),
                'properties' : ('properties', True, None),
                'decodings' : ('decodings', True, None),
            },
        },
        'properties': {
            'type' : list,
            'item_type' : 'property',
        },
        'property' : {
            'type' : tuple,
            'length' : '4',
            '0' : (str, True, '^[a-z_]+$'),                     # name
            '1' : (str, True, '^[a-z_]+\.?[a-z_]+$'),           # type
            '2' : (str, True, ['0.1', '0.N', '1.1', '1.N']),    # cardinality
            '3' : (str, False, None),                           # doc
        },
        'decodings': {
            'type' : list,
            'item_type' : 'decoding',
        },
        'decoding' : {
            'type' : tuple,
            'length' : '2|3',
            '0' : (str, True, '^[a-z_]+$'),                     # name
            '1' : (str, True, None),                            # decoding
            '2' : (str, True, '^[a-z_]+\.?[a-z_]+$'),           # sub-type
        },
        'enums': {
            'type' : list,
            'item_type' : 'enum',
        },
        'enum' : {
            'type' : dict,
            'fields' : {
                'name' : (str, True, '^[a-z_]+$'),
                'is_open' : (bool, True, None),
                'doc' : (str, False, None),
                'members' : ('enum_members', True, None),
            },
        },
        'enum_members': {
            'type' : list,
            'item_type' : 'enum_member',
        },
        'enum_member' : {
            'type' : tuple,
            'length' : '2',
            'fields' : {
                '0' : (str, True, '^[a-z-A-Z]+$'),          # name
                '1' : (str, False, None),                   # doc
            },
        },
    }


def _get_error(error, ctx):
    """Returns formatted error mesage.

    Keyword Arguments:
    error - validationn error.
    ctx - validation context.

    """
    pass


def _set_error(ctx, error):
    """Appends an error to managed collection.

    Keyword Arguments:
    ctx - validation context.
    error - a validation error.

    """
    if error is not None:
        if isinstance(error, list):
            ctx['errors'] += error
        else:
            ctx['errors'].append(error)
        

def _validate_field(field, field_data, field_elem, ctx):
    """Validates configuration data against passed dictionary configuration element.

    Keyword Arguments:
    data - data being validated.
    elem - dictionary configuration element that data is associatd with.
    ctx - validation context.

    """
    errors = []
    schema = _get_schema()

    # Unpack field attributes.
    field_type, field_value_required, field_validator = field_elem

    # Field value required validation.
    if field_data is None:
        if field_value_required:
            _set_error(ctx, 'Required field value :: {0}.'.format(field))

    # Simple field validation.
    elif field_type not in schema:
        # ... field type validation.
        if not isinstance(field_data, field_type):
            _set_error(ctx, '{0} value is of an invalid type (expected {1}).'.format(field_data, field_type))
        elif field_validator is not None:
            if isinstance(field_validator, list) and field_data not in field_validator:
                _set_error(ctx, '{0} value ({1}) is not permitted value :: expected one of {2}.'.format(field, field_data, field_validator))
            elif re.match(field_validator, field_data) is None:
                _set_error(ctx, '{0} format is invalid :: {1}.'.format(field, field_data))

    # Complex field validation.
    else:
        # ... field type validation.
        field_sub_type = schema[field_type]['type']
        if not isinstance(field_data, field_sub_type):
            _set_error(ctx, 'Invalid field type :: {0} (expected {1}).'.format(field, field_sub_type))
        # ... recurse sub-fields.
        else:
            _set_error(ctx, _validate(field_data, field_type, ctx))

    return errors


def _validate_dict(cfg, cfg_schema, ctx):
    """Validates configuration data against passed dictionary configuration element.

    Keyword Arguments:
    cfg - configuration being validated.
    cfg_schema - configuration schema.
    ctx - validation context.

    """
    errors = []

    elem_fields = cfg_schema['fields']
    for field in elem_fields:
        # Field required validation.
        if field not in cfg:
            _set_error(ctx, 'Required field :: {0}.'.format(field))
        # Other field level validation.
        else:
            field_data = cfg[field]
            field_elem = elem_fields[field]
            _set_error(ctx, _validate_field(field, field_data, field_elem, ctx))

    return errors


def _validate_list(cfg, cfg_schema, ctx):
    """Validates configuration data against passed list configuration element.

    Keyword Arguments:
    cfg - configuration being validated.
    cfg_schema - configuration schema.
    ctx - validation context.

    """
    errors = []

    item_elem_name = cfg_schema['item_type']
    for item_data in cfg:
        _set_error(ctx, _validate(item_data, item_elem_name, ctx))

    return errors


def _validate_tuple(cfg, cfg_schema, ctx):
    """Validates configuration data against passed tuple configuration element.

    Keyword Arguments:
    cfg - configuration being validated.
    cfg_schema - configuration schema.
    ctx - validation context.

    """
    errors = []

    if len(cfg) not in map(int, cfg_schema['length'].split('|')):
        _set_error(ctx, 'Invalid tuple length.')

    return errors


def _validate(cfg, cfg_type_name, ctx):
    """Validates configuration data against passed configuration element.

    Keyword Arguments:
    cfg - configuration being validated.
    cfg_type_name - name of configuration schema type (E.G. ontology).
    ctx - validation context.

    """
    errors = []
    schema = _get_schema()

    if cfg_type_name not in schema:
        _set_error(ctx, 'Configuration element unsupported :: {0}.'.format(cfg_type_name))
    else:
        cfg_schema = schema[cfg_type_name]
        cfg_type = cfg_schema['type']
        if isinstance(cfg, cfg_type) == False:
            _set_error(ctx, 'Configuration element type invalid :: {0} (expected {1}).'.format(cfg_schema, cfg_type))
        else:
            if cfg_type == dict:
                _set_error(ctx, _validate_dict(cfg, cfg_schema, ctx))
            elif cfg_type == list:
                _set_error(ctx, _validate_list(cfg, cfg_schema, ctx))
            elif cfg_type == tuple:
                _set_error(ctx, _validate_tuple(cfg, cfg_schema, ctx))

    return errors


def validate_ontology_schema(ontology_schema):
    """Validates ontology schema.

    :param ontology_schema: Ontology schema definition.
    :type ontology_schema: dict
    :returns: List of validation errors (if any).
    :rtype: list

    """
    errors = []
    
    if not isinstance(ontology_schema, dict):
        errors.append('Ontology schema is not a python dictionary.')
    else:
        pass

    return errors


def validate_language(language):
    """Returns list of target programming language validation errors.

    :param language: Target programming language.
    :type language: str
    :returns: List of validation errors (if any).
    :rtype: list

    """
    errors = []
    
    if not language in _LANGUAGES:
        errors.append('Programming language is unsupported [{0}].  Supported languages are {1}.'.format(language, _LANGUAGES))

    return errors


def validate_output_dir(output_dir):
    """Returns list of target output directory validation errors.

    :param output_dir: Target output directory.
    :type output_dir: str
    :returns: List of validation errors (if any).
    :rtype: list

    """
    errors = []

    if not os.path.exists(output_dir):
        errors.append('Output directory does not exist [{0}].'.format(output_dir))

    return errors