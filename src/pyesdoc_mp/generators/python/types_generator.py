"""
.. module:: pyesdoc_mp.generators.python.types_generator.py
   :platform: Unix, Windows
   :synopsis: Generates code to represent an ontology as a set of types.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
from pyesdoc_mp.generators.generator import Generator
from pyesdoc_mp.generators.generator_utils import (
    emit_indent,
    emit_line_return,
    get_template
    )
from pyesdoc_mp.generators.python.utils import (
    get_class_base_name,
    get_class_file_name,
    get_class_import_name,
    get_class_name,
    get_enum_name,
    get_enum_file_name,
    get_ontology_directory,
    get_ontology_name,
    get_ontology_version,
    get_package_directory,
    get_package_init_file_name,
    get_package_name,
    get_package_path,
    get_property_ctor,
    get_property_field_name,
    get_property_name,
    get_type_doc_name,
    get_type_functional_name
    )



# Template for a concrete class.
_TEMPLATE_CLASS_CONCRETE = "class_concrete.txt"

# Template for an abstract class.
_TEMPLATE_CLASS_ABSTRACT = "class_abstract.txt"

# Template for an abstract class.
_TEMPLATE_CLASS_REPRESENTATIONS = "class_representations.txt"

# Template for an enumeration.
_TEMPLATE_ENUM = "enum.txt"

# Template for package.
_TEMPLATE_PACKAGE = "package.txt"

# Template for sub package.
_TEMPLATE_PACKAGE_SUB = "package_sub.txt"


class TypesGenerator(Generator):
    """Generates code to represent an ontology as a set of types.

    """
    def on_ontology_parse(self, ctx):
        """Event handler for the ontology parse event.

        :param ctx: Generation context information.
        :type ctx: pyesdoc_mp.generators.generator.GeneratorContext

        """
        # Helper functions.
        def emit_imports():
            return self.emit_imports_for_root_package(ctx)

        code = self.emit_package_init_file(ctx, _TEMPLATE_PACKAGE, emit_imports)
        dir = get_ontology_directory(ctx, 'types')
        file = get_package_init_file_name()

        return (code, dir, file)



    def on_package_parse(self, ctx):
        """Event handler for the package parse event.

        :param ctx: Generation context information.
        :type ctx: pyesdoc_mp.generators.generator.GeneratorContext

        """
        # Helper functions.
        def emit_imports():
            return self.emit_imports_for_sub_package(ctx)

        code = self.emit_package_init_file(ctx, _TEMPLATE_PACKAGE_SUB, emit_imports)
        dir = get_package_directory(ctx.pkg, ctx.output_dir, 'types')
        file = get_package_init_file_name()

        return (code, dir, file)


    def on_class_parse(self, ctx):
        """Event handler for the class parse event.

        :param ctx: Generation context information.
        :type ctx: pyesdoc_mp.generators.generator.GeneratorContext

        """
        code = self.emit_class(ctx)
        dir = get_package_directory(ctx.pkg, ctx.output_dir, 'types')
        file = get_class_file_name(ctx.cls)
        
        return (code, dir, file)


    def on_enum_parse(self, ctx):
        """Event handler for the enum parse event.

        :param ctx: Generation context information.
        :type ctx: pyesdoc_mp.generators.generator.GeneratorContext

        """
        code = self.emit_enum(ctx)
        dir = get_package_directory(ctx.pkg, ctx.output_dir, 'types')
        file = get_enum_file_name(ctx.enum)
        
        return (code, dir, file)


    def emit_package_init_file(self, ctx, template, package_imports_fn):
        """Emits a package initialisation file.

        :param ctx: Generation context information.
        :param template: Code template.
        :param package_imports_fn: Package imports generator callback.
        :type ctx: pyesdoc_mp.generators.generator.GeneratorContext
        :type template: str
        :type package_imports_fn: function

        """
        code = get_template(ctx, template)

        if ctx.pkg is not None:
            code = code.replace('{package-name}', get_package_name(ctx.pkg))
        code = code.replace('{module-imports}', package_imports_fn())

        return code


    def emit_imports_for_root_package(self, ctx):
        """Emits code corresponding to a set of root package imports.

        :param ctx: Generation context information.
        :type ctx: pyesdoc_mp.generators.generator.GeneratorContext
        
        """
        code = ''

        for pkg in ctx.ontology.packages:
            code += self.emit_imports_for_sub_package(ctx, pkg)
            
        return code


    def emit_imports_for_sub_package(self, ctx, pkg=None):
        """Emits code corresponding to a set of sub package imports.

        :param ctx: Generation context information.
        :type ctx: pyesdoc_mp.generators.generator.GeneratorContext

        """
        code = ''

        pkg = pkg if pkg is not None else ctx.pkg
        for cls in pkg.classes:
            code += 'from py{0}.v{1}.types.{2}.{3} import {4}{5}'.format(
                get_ontology_name(ctx.ontology),
                get_ontology_version(ctx.ontology),
                get_package_name(pkg),
                get_class_import_name(cls),
                get_class_name(cls),
                emit_line_return())
                
        return code


    def emit_class(self, ctx):
        """Emits code corresponding to a python class.

        :param ctx: Generation context information.
        :type ctx: pyesdoc_mp.generators.generator.GeneratorContext

        """
        # Set helper vars.
        class_imports = self.emit_class_imports(ctx, ctx.cls.imports)
        class_circular_imports = self.emit_class_imports(ctx, ctx.cls.circular_imports)
        class_properties = self.emit_class_properties(ctx)
        class_property_constants = self.emit_class_property_constants(ctx)
        class_representations = self.emit_class_representations(ctx)

        # Open template.
        if ctx.cls.is_abstract:
            code = get_template(ctx, _TEMPLATE_CLASS_ABSTRACT)
        else:
            code = get_template(ctx, _TEMPLATE_CLASS_CONCRETE)

        # Generate code.        
        code = code.replace('{package-name}', get_package_name(ctx.pkg))
        code = code.replace('{class-name}', get_class_name(ctx.cls))
        code = code.replace('{base-class-name}', get_class_base_name(ctx.cls.base))
        code = code.replace('{class-doc-string}', ctx.cls.doc_string)
        code = code.replace('{class_constants}', class_property_constants)
        code = code.replace('{class-imports}', class_imports)
        code = code.replace('{class-circular-imports}', class_circular_imports)
        code = code.replace('{class-properties}', class_properties)
        code = code.replace('{class-representations}', class_representations)

        return code


    def emit_enum(self, ctx):
        """Emits code corresponding to a python class.

        :param ctx: Generation context information.
        :type ctx: pyesdoc_mp.generators.generator.GeneratorContext

        """
        code = get_template(ctx, _TEMPLATE_ENUM)

        code = code.replace('{enum-name}', get_enum_name(ctx.enum))
        code = code.replace('{enum-doc-string}', ctx.enum.doc_string)

        return code


    def emit_class_properties(self, ctx):
        """Emits set of class properties.

        :param ctx: Generation context information.
        :type ctx: pyesdoc_mp.generators.generator.GeneratorContext

        """
        code = ''
        prp_ctor = ''
        tmpl = '{0}{1}{2}# type = {3}{4}'

        # Initialise property fields.
        for prp in ctx.cls.properties:
            prp_ctor = get_property_ctor(prp)
            if code == '':
                code += emit_line_return(1)
            code += tmpl.format(emit_indent(2),
                                prp_ctor,
                                ''.ljust(45 - len(prp_ctor)),
                                get_type_doc_name(prp.type),
                                emit_line_return())

        return code


    def emit_class_property_constants(self, ctx):
        """Emits set of class property constants.

        :param ctx: Generation context information.
        :type ctx: pyesdoc_mp.generators.generator.GeneratorContext

        """
        code = ''
        tmpl = '{0}self.{1} = {2}("{3}"){4}'

        # Assign constants.
        for cnt in ctx.cls.constants:
            prp = ctx.cls.get_property(cnt[0])
            if prp is not None:
                if code == '':
                    code += emit_line_return(1)
                code += tmpl.format(emit_indent(2),
                                    cnt[0],
                                    get_type_functional_name(prp.type),
                                    cnt[1],
                                    emit_line_return())
            
        return code


    def emit_class_imports(self, ctx, imports):
        """Emits code corresponding to a set of python class imports.

        :param ctx: Generation context information.
        :param imports: Imports being parsed.
        :type ctx: pyesdoc_mp.generators.generator.GeneratorContext
        :type imports: list

        """
        code = ''
        tmpl = 'from py{0}.{1} import {2}'

        for package, type in imports:
            pkg_path = get_package_path(ctx.ontology, 'types', package)
            type_name = get_class_name(type)
            type_import_name = get_class_import_name(type)
            code += tmpl.format(pkg_path, type_import_name, type_name)
            code += emit_line_return()

        return code


    def emit_class_representations(self, ctx):
        """Emits code corresponding to the set of representations of the class.

        :param ctx: Generation context information.
        :type ctx: pyesdoc_mp.generators.generator.GeneratorContext

        """
        # For now there is only a dictionary representation.
        return self.emit_class_representation_as_dict(ctx);


    def emit_class_representation_as_dict(self, ctx):
        """Emits code corresponding to a dictionary representation of the class.

        :param ctx: Generation context information.
        :type ctx: pyesdoc_mp.generators.generator.GeneratorContext

        """
        # Set dict ctor.
        dict_ctor = ''
        if ctx.cls.base is not None:
            dict_ctor = 'super({class-name}, self).as_dict()'

        # Set dict items.
        dict_items = ''
        for prp in ctx.cls.properties:
            dict_items += "{0}append(d, '{1}', {2}, {3}, {4}, {5})".format(
                emit_line_return() + emit_indent(2),
                get_property_name(prp),
                get_property_field_name(prp),
                prp.is_iterative,
                prp.type.is_simple,
                prp.type.is_enum)

        # Open template.
        code = get_template(ctx, _TEMPLATE_CLASS_REPRESENTATIONS)

        # Generate code.
        code = code.replace('{dict-ctor}', dict_ctor)
        code = code.replace('{dict-items}', dict_items)
        code = code.replace('{class-name}', get_class_name(ctx.cls))

        return code

