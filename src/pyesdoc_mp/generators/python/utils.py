"""Encapsualtes a set of python specific name conversion operations.

"""
# Module imports.
from operator import add

from pyesdoc_mp.utils.generation import *



# Language name constant.
LANGUAGE = 'python'

# Language prefix constant.
LANGUAGE_PREFIX = 'py'

# Language file extension constant.
FILE_EXTENSION = '.py'

# Python package initialisation file name.
_PACKAGE_INIT_FILE = '__init__'

# Python clas property field prefix.
_PROPERTY_FIELD_PREFIX = 'self.'

# Set of simple type mappings.
_SIMPLE_TYPE_MAPPINGS = {
    'bool' : 'bool',
    'date' : 'datetime.date',
    'datetime' : 'datetime.datetime',
    'float' : 'float',
    'int' : 'int',
    'str' : 'str',
    'uri' : 'str',
    'uuid' : 'uuid.UUID',
}

# Simple type null value.
_SIMPLE_NULL_VALUES = {
    'bool' : 'bool()',
    'datetime.date' : 'datetime.date(1900, 1, 1)',
    'datetime.datetime' : 'datetime.datetime.now()',
    'float' : 'float()',
    'int' : 'int()',
    'str' : 'str()',
    'uri' : 'str()',
    'uuid.UUID' : 'uuid.uuid4()',
}

# Set of simple type default values.
_SIMPLE_DEFAULT_VALUES = {
    'bool' : 'bool()',
    'datetime.date' : 'datetime.date(1900, 1, 1)',
    'datetime.datetime' : 'datetime.datetime.now()',
    'float' : 'float()',
    'int' : 'int()',
    'str' : 'str()',
    'uri' : 'str()',
    'uuid.UUID' : 'uuid.uuid4()',
}

# Iterative type default value.
_ITERATIVE_DEFAULT_VALUE = '[]'

# Iterative type null value.
_ITERATIVE_NULL_VALUE = '[]'

# Complex enum default value.
_ENUM_DEFAULT_VALUE = "''"

# Complex enum null value.
_ENUM_NULL_VALUE = "''"

# Complex type null value.
_CLASS_NULL_VALUE = 'None'


def _strip(name):
    """Returns stripped name.

    Keyword Arguments:
    name - name being converted.

    """
    if isinstance(name, str) == False:
        name = name.name
    return name


def _strip_class_name(name):
    """Returns stripped class name.

    Keyword Arguments:
    name - name being converted.

    """
    name = _strip(name)
    if name.find('.') != -1:
        name = name.split('.')[len(name.split('.')) - 1]
    return name


def get_ontology_name(name):
    """Converts name to a python ontology name.

    Keyword Arguments:
    name - name being converted.

    """
    if isinstance(name, str) == False:
        name = name.name

    return name.lower()


def get_ontology_version(name):
    """Converts version identifier to a python ontology version.

    Keyword Arguments:
    name - name of version identifier being converted.

    """
    if isinstance(name, str) == False:
        name = name.version

    return name.replace(".", "_")


def _get_ontology_directory(ontology, root=None, sub=None, suffix_root=False):
    """Returns ontology directory into which code is generated code.

    Keyword Arguments:
    ontology - ontology being processed.
    root - root directory with which ontology is associated.
    sub - sub directory to append as a suffix.
    suffix_root_dir - flag indicating whether to append a standard suffix to root directory.

    """
    dir = ''
    if root is not None:
        dir += root + '/'
    if suffix_root == True:
        dir += 'cim_codegen/python/'
        dir += get_ontology_name(ontology)
    dir += get_ontology_name(ontology)
    dir += '/'
    dir += 'v' + get_ontology_version(ontology)
    if sub is not None:
        dir += '/' + sub
    return dir


def get_ontology_directory(ctx, sub=None, include_version=True):
    """Returns ontology directory into which code is generated code.

    :param ctx: Generation context information.
    :param sub: Subpackage name.
    :type ctx: pyesdoc_mp.generators.generator.GeneratorContext
    :type sub: str

    """
    dir = ''
    if ctx.output_dir is not None:
        dir += ctx.output_dir + '/'
    dir += get_ontology_name(ctx.ontology)
    if include_version:
        dir += '/'
        dir += 'v' + get_ontology_version(ctx.ontology)
    if sub is not None:
        dir += '/'
        dir += sub
    return dir


def get_package_name(name):
    """Converts name to a python package name.

    Keyword Arguments:
    name - name being converted.

    """
    name = _strip_package_name(name)
    return name


def get_package_path(ontology, parent, package):
    """Returns full python package name.

    Keyword Arguments:
    name - name being converted.

    """
    result = get_ontology_name(ontology)
    result += '.v'
    result += get_ontology_version(ontology)
    result += '.'
    result += get_package_name(parent)
    result += '.'
    result += get_package_name(package)
    return result


def get_package_directory(package, root=None, sub=None, suffix_root=False):
    """Returns package directory into which code is generated code.

    Keyword Arguments:
    package - package being processed.
    root_dir - root directory with which package is associated.
    sub_dir - sub directory.
    suffix_root_dir - flag indicating whether to append a standard suffix to root directory.

    """
    dir = _get_ontology_directory(package.ontology, root, sub, suffix_root)
    dir += '/'
    dir += get_package_name(package)
    return dir


def get_class_name(name):
    """Converts name to a python class name.

    Keyword Arguments:
    name - name being converted.

    """
    name = _strip_class_name(name)
    return convert_to_camel_case(name)


def get_class_import_name(name):
    """Converts name to a python class import name.

    Keyword Arguments:
    name - name being converted.

    """
    name = _strip_class_name(name)
    return name


def get_class_functional_name(name):
    """Converts name to one suitable for use in a python function definition.

    Keyword Arguments:
    name - name being converted.

    """
    name = _strip_class_name(name)
    return name


def get_class_doc_string_name(name):
    """Converts name to one suitable for use in python documentation.

    Keyword Arguments:
    name - name being converted.

    """
    name = _strip_class_name(name)
    return name.replace('_', ' ')


def get_class_file_name(name):
    """Converts name to a python class file name.

    Keyword Arguments:
    name - name being converted.

    """
    name = _strip_class_name(name)
    return name + FILE_EXTENSION


def get_class_base_name(name):
    """Converts name to a python base class name.

    Keyword Arguments:
    name - name being converted.

    """
    if name is not None:
        return get_class_name(name)
    else:
        return 'object'


def get_property_ctor(prp):
    """Converts class property to a python property constructor declaration.

    Keyword Arguments:
    name - name being converted.

    """
    return 'self.{0} = {1}'.format(get_property_name(prp),
                                   get_property_default_value(prp))


def get_property_name(name):
    """Converts name to a python class property name.

    Keyword Arguments:
    name - name being converted.

    """
    name = _strip(name)
    return name


def get_property_field_name(name):
    """Converts name to a python class property field name.

    Keyword Arguments:
    name - name being converted.

    """
    name = _strip(name)
    return _PROPERTY_FIELD_PREFIX + name


def _get_default_value(type_name, is_simple, is_iterative, is_required, is_enum):
    """Returns default type value.

    """
    # Iterables: convert via pre-defined mappings.
    if is_iterative:
        if is_required:
            return _get_iterative_default_value()
        else:
            return _get_iterative_null_value()
    # Simple types: convert via pre-defined mappings.
    elif is_simple:
        if is_required:
            return _get_simple_default_value(type_name)
        else:
            return _get_simple_null_value(type_name)
    # Enum types: .
    elif is_enum:
        if is_required:
            return _get_enum_default_value(type_name)
        else:
            return _get_enum_null_value(type_name)
    # Class types: convert via pre-defined mappings.
    else:
        if is_required:
            return _get_class_default_value(type_name)
        else:
            return _get_class_null_value(type_name)


def get_property_default_value(property):
    """Returns property default value.

    """
    return _get_default_value(get_type_name(property.type),
                              property.type.is_simple,
                              property.is_iterative,
                              property.is_required,
                              property.type.is_enum)


def get_type_name(type):
    """Returns python type name.

    Keyword Arguments:
    type - a type declaration.

    """
    name = type.name
    if type.is_simple:
        return _get_simple_type_mapping(name)
    elif type.is_enum:
        return _get_simple_type_mapping('str')
    elif type.is_complex:
        return get_class_name(name)


def get_type_functional_name(type):
    """Returns python type functional name.

    Keyword Arguments:
    type - a type declaration.

    """
    name = type.name
    if type.is_simple:
        return name
    elif type.is_enum:
        return 'str'
    elif type.is_complex:
        return get_class_name(name)


def get_type_doc_name(type):
    """Returns python type documentation name.

    Keyword Arguments:
    type - a type declaration.

    """
    name = type.name
    if type.is_simple:
        return _get_simple_type_mapping(name)
    elif type.is_enum:
        return '{0}.{1}'.format(get_package_name(name), get_enum_name(name))
    elif type.is_complex:
        return '{0}.{1}'.format(get_package_name(name), get_class_name(name))


def _strip_enum_name(name):
    """Returns stripped enum name.

    Keyword Arguments:
    name - name being converted.

    """
    name = _strip(name)
    if name.find('.') != -1:
        name = name.split('.')[len(name.split('.')) - 1]
    return name


def get_enum_name(name):
    """Converts name to a python enum name.

    Keyword Arguments:
    name - name being converted.

    """
    name = _strip_enum_name(name)
    return convert_to_camel_case(name)


def get_enum_file_name(name):
    """Converts name to a python enum file name.

    Keyword Arguments:
    name - name being converted.

    """
    name = _strip_enum_name(name)
    return name + FILE_EXTENSION


def _get_simple_type_mapping(simple):
    """Returns matching simple type mapping.

    Keyword Arguments:
    simple - simple type name.

    """
    return _SIMPLE_TYPE_MAPPINGS[simple]


def _get_simple_default_value(simple):
    """Returns default value of a simple type.

    Keyword Arguments:
    simple - simple type name.

    """
    return _SIMPLE_DEFAULT_VALUES[simple]


def _get_simple_null_value(simple):
    """Returns null value of a simple type.

    Keyword Arguments:
    simple - simple type name.

    """
    return _SIMPLE_NULL_VALUES[simple]


def _get_iterative_default_value():
    """Returns default value of an iterative type.

    """
    return _ITERATIVE_DEFAULT_VALUE


def _get_iterative_null_value():
    """Returns null value of an iterative type.

    """
    return _ITERATIVE_NULL_VALUE


def _get_enum_default_value(enum):
    """Returns default value of a complex enum type.

    Keyword Arguments:
    enum - complex enum type name.

    """
    return _ENUM_DEFAULT_VALUE


def _get_enum_null_value(enum):
    """Returns null value of a complex enum type.

    Keyword Arguments:
    enum - complex enum type name.

    """
    return _ENUM_NULL_VALUE


def _get_class_default_value(complex):
    """Returns default value of a complex type.

    Keyword Arguments:
    complex - complex type name.

    """
    return 'None'
    return complex + '()'


def _get_class_null_value(complex):
    """Returns null value of a complex type.

    """
    return _CLASS_NULL_VALUE


def _strip_package_name(name):
    """Returns stripped package name.

    Keyword Arguments:
    name - name being converted.

    """
    name = _strip(name)
    if name.find('.') != -1:
        name = name.split('.')[0]
    return name


def get_package_init_file_name():
    """Returns python package init file name.

    Keyword Arguments:
    name - name being converted.

    """
    return _PACKAGE_INIT_FILE + FILE_EXTENSION



def get_package_module_name(name, prefix):
    """Returns a package module name by injecting package name into a template.

    :param name: A package name, e.g. "types".
    :param prefix: A package name prefix, e.g. "validator".
    :type name: str
    :type prefix: str

    """
    return (prefix + "_for_{0}_package").format(get_package_name(name))


def get_package_module_file_name(name, prefix):
    """Returns a package module file name by injecting package name into a template.

    :param name: A package name, e.g. "types".
    :param prefix: A package name prefix, e.g. "validator".
    :type name: str
    :type prefix: str

    """
    return get_package_module_name(name, prefix) + FILE_EXTENSION
   
