"""
.. module:: pyesdoc_mp.generators.python.decoding_generator.py
   :platform: Unix, Windows
   :synopsis: Generates code to support serialization.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
from operator import add

from pyesdoc_mp.generators.generator import Generator
from pyesdoc_mp.generators.generator_utils import (
    emit_indent,
    emit_line_return,
    get_template
    )
from pyesdoc_mp.generators.python.utils import (
    get_class_name,
    get_class_functional_name,
    get_class_doc_string_name,
    get_ontology_directory,
    get_ontology_name,
    get_ontology_version,
    get_package_init_file_name,
    get_package_module_file_name,
    get_package_module_name,
    get_package_name,
    get_type_functional_name
    )
    


# Template for a decoder module.
_TEMPLATE_DECODER_MODULE = 'decoder_module.txt'

# Template for a decoder function.
_TEMPLATE_DECODER_FUNCTION = "decoder_function.txt"

# Template for package.
_TEMPLATE_PACKAGE = "package.txt"





def get_class_decoder_function_name(name):
    """Converts name to a python class decoder function name.

    Keyword Arguments:
    name - name being converted.

    """
    name = get_class_functional_name(name)
    return 'decode_{0}'.format(name)


class DecodingGenerator(Generator):
    """Generates code to support serialization.

    """
    def on_start(self, ctx):
        """Event handler for the parsing start event.

        :param ctx: Generation context information.
        :type ctx: pyesdoc_mp.generators.generator.GeneratorContext

        """
        self.output_dir = get_ontology_directory(ctx, 'serialization')


    def on_ontology_parse(self, ctx):
        """Event handler for the ontology parse event.

        :param ctx: Generation context information.
        :type ctx: pyesdoc_mp.generators.generator.GeneratorContext

        """
        code = self.emit_root_init_file(ctx)
        dir = self.output_dir
        file = get_package_init_file_name()

        return (code, dir, file)


    def on_package_parse(self, ctx):
        """Event handler for the package parse event.

        :param ctx: Generation context information.
        :type ctx: pyesdoc_mp.generators.generator.GeneratorContext

        """
        def get_imports():
            imports = []

            def append_import(imp):
                if imp not in imports:
                    imports.append(imp)

            # Set package class type imports.
            imp = 'from {0}.v{1}.types.{2} import *'.format(
                get_ontology_name(ctx.ontology),
                get_ontology_version(ctx.ontology),
                get_package_name(ctx.pkg))
            append_import(imp)

            # Set type decoding imports.
            for type in [t for t in ctx.pkg.external_types if t.is_class]:
                imp = 'from {0}.v{1}.serialization.{2} import *'.format(
                    get_ontology_name(ctx.ontology),
                    get_ontology_version(ctx.ontology),
                    get_package_module_name(type.name_of_package, 'decoder'))
                append_import(imp)

            if len(imports) > 0:
                return reduce(add, map(lambda i : i + emit_line_return(), sorted(imports)))
            else:
                return ''

        def get_functions():
            fns = ''
            for cls in ctx.pkg.classes:
                dcs = self.get_decodings(cls)
                fn = get_template(ctx, _TEMPLATE_DECODER_FUNCTION)
                fn = fn.replace('{class-name}', get_class_name(cls))
                fn = fn.replace('{class-function-name}', get_class_functional_name(cls))
                fn = fn.replace('{class-doc-name}', get_class_doc_string_name(cls))
                fn = fn.replace('{class-decodings}', dcs)
                fn += emit_line_return(3)
                fns += fn
            return fns

        code = get_template(ctx, _TEMPLATE_DECODER_MODULE)
        code = code.replace('{module-imports}', get_imports())
        code = code.replace('{decoding-functions}', get_functions())
        dir = self.output_dir
        file = get_package_module_file_name(ctx.pkg, 'decoder')

        return (code, dir, file)


    def get_decodings(self, cls):
        """Returns class level decodings.

        :param cls: Ontology class being processed.
        :type cls: pyesdoc_mp.ontology.class_.Class

        """
        code = ''
        for p in cls.all_properties:
            for dc in cls.get_property_decodings(p):
                if dc.decoding is not None:
                    code += self.emit_decoding(p, dc.decoding, dc.type)
        return code


    def emit_decoding(self, prp, decoding, type):
        """Emits code corresponding to a class property decoding.

        :param prp: Ontology class property definition.
        :param decoding: Ontology class property decoding definition.
        :param type: Ontology class property type definition.
        :type prp: pyesdoc_mp.ontology.property.Property
        :type decoding: pyesdoc_mp.ontology.decoding.Decoding
        :type type: pyesdoc_mp.ontology.type.Type

        """
        def get_decoding_function():
            # ... simple/enum types - return type functional name
            #     (is directly mapped to a convertor function).
            if prp.type.is_simple or prp.type.is_enum:
                return '\'{0}\''.format(get_type_functional_name(prp.type))
            # ... complex classes - return class functional name.
            elif prp.type.is_class:
                type_name = prp.type.name if type is None else type
                return get_class_decoder_function_name(type_name)

        tmpl = '{0}(\'{1}\', {2}, {3}, \'{4}\'),'
        return tmpl.format(
            emit_line_return() + emit_indent(2),
            prp.name,
            prp.is_iterative,
            get_decoding_function(),
            '' if decoding is None else decoding)


    def emit_root_init_file(self, ctx):
        """Emits package initialisation file.

        :param ctx: Generation context information.
        :type ctx: pyesdoc_mp.generators.generator.GeneratorContext

        """
        def get_imports():
            imports = ''
            is_first = True
            tmpl = "from {0}.v{1}.serialization.{2} import {3}"

            for e in ctx.ontology.entities:
                if not is_first:
                    imports += emit_line_return()
                imports += tmpl.format(
                    get_ontology_name(ctx.ontology),
                    get_ontology_version(ctx.ontology),
                    get_package_module_name(e.package, 'decoder'),
                    get_class_decoder_function_name(e))
                is_first = False
                
            return imports

        code = get_template(ctx, _TEMPLATE_PACKAGE)
        code = code.replace('{module-imports}', get_imports())

        return code
