"""
.. module:: pyesdoc_mp.generators.python.validation_generator.py
   :platform: Unix, Windows
   :synopsis: Generates code to perform type instance validation.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
from operator import add

from pyesdoc_mp.generators.generator import Generator
from pyesdoc_mp.utils.generation import (
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
    get_package_name
    )
    


# Template for a validator module.
_TEMPLATE_VALIDATOR_MODULE = 'validator_module.txt'

# Template for a validator function.
_TEMPLATE_VALIDATOR_FUNCTION = "validator_function.txt"

# Template for package.
_TEMPLATE_PACKAGE = "package.txt"


def get_class_validator_function_name(name):
    """Converts name to a python class validator function name.

    Keyword Arguments:
    name - name being converted.

    """
    name = get_class_functional_name(name)
    return 'validate_{0}'.format(name)


class ValidationGenerator(Generator):
    """Generates code to perform type instance validation.

    """
    def on_start(self, ctx):
        """Event handler for the parsing start event.

        :param ctx: Generation context information.
        :type ctx: pyesdoc_mp.generators.generator.GeneratorContext

        """
        self.output_dir = get_ontology_directory(ctx, 'validation')


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
            imp = 'from py{0}.v{1}.types.{2} import *'.format(
                get_ontology_name(ctx.ontology),
                get_ontology_version(ctx.ontology),
                get_package_name(ctx.pkg))
            append_import(imp)

            # Set type decoding imports.
            for type in [t for t in ctx.pkg.external_types if t.is_class]:
                imp = 'from py{0}.v{1}.validation.{2} import *'.format(
                    get_ontology_name(ctx.ontology),
                    get_ontology_version(ctx.ontology),
                    get_package_module_name(type.name_of_package, 'validator'))
                append_import(imp)

            if len(imports) > 0:
                return reduce(add, map(lambda i : i + emit_line_return(), sorted(imports)))
            else:
                return ''


        def get_functions():
            fns = ''
            for cls in ctx.pkg.classes:
                fn = get_template(ctx, _TEMPLATE_VALIDATOR_FUNCTION)
                fn = fn.replace('{class-name}', get_class_name(cls))
                fn = fn.replace('{class-function-name}', get_class_functional_name(cls))
                fn = fn.replace('{class-doc-name}', get_class_doc_string_name(cls))
                fn += emit_line_return(3)
                fns += fn
            return fns
        

        code = get_template(ctx, _TEMPLATE_VALIDATOR_MODULE)
        code = code.replace('{module-imports}', get_imports())
        code = code.replace('{validation-functions}', get_functions())
        code = code.replace('{package-name}', get_package_name(ctx.pkg))
        dir = self.output_dir
        file = get_package_module_file_name(ctx.pkg, 'validator')

        return (code, dir, file)


    def emit_root_init_file(self, ctx):
        """Emits package initialisation file.

        :param ctx: Generation context information.
        :type ctx: pyesdoc_mp.generators.generator.GeneratorContext

        """
        def get_imports():
            imports = ''
            is_first = True
            tmpl = "from py{0}.v{1}.validation.{2} import {3}"

            for cls in ctx.ontology.classes:
                if not is_first:
                    imports += emit_line_return()
                imports += tmpl.format(
                    get_ontology_name(ctx.ontology),
                    get_ontology_version(ctx.ontology),
                    get_package_module_name(cls.package, 'validator'),
                    get_class_validator_function_name(cls))
                is_first = False
                
            return imports

        code = get_template(ctx, _TEMPLATE_PACKAGE)
        code = code.replace('{module-imports}', get_imports())
        
        return code
