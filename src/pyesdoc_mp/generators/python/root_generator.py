"""
.. module:: pyesdoc_mp.generators.python.root_generator.py
   :platform: Unix, Windows
   :synopsis: Generates root package initialisation code.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
from pyesdoc_mp.generators.generator import Generator
from pyesdoc_mp.utils.generation import get_template
from pyesdoc_mp.generators.python.utils import (
    get_ontology_directory,
    get_package_init_file_name
    )



# Template for package.
_TEMPLATE_PACKAGE_1 = 'package_1.txt'

# Template for package.
_TEMPLATE_PACKAGE_2 = 'package_2.txt'


class RootGenerator(Generator):
    """Generates root level packages.

    """
    
    def on_ontology_parse(self, ctx):
        """Event handler for the ontology parse event.

        :param ctx: Generation context information.
        :type ctx: pyesdoc_mp.generators.generator.GeneratorContext

        """
        def get_code(template, include_version):
            return (get_template(ctx, template), \
                    get_ontology_directory(ctx, include_version=include_version), \
                    get_package_init_file_name())

        return [
            get_code(_TEMPLATE_PACKAGE_1, False),
            get_code(_TEMPLATE_PACKAGE_2, True)
        ]

