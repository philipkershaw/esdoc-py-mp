"""
.. module:: pyesdoc_mp.generate.py
   :copyright: Copyright "Feb 7, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: pyesdoc_mp code generator.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

import optparse

from pyesdoc_mp import generate
from pyesdoc_mp.utils.factory import create_ontology_schema


def _get_options():
    """Returns command line options.

    :returns: Command line options.
    :rtype: dict

    """
    p = optparse.OptionParser(prog="ES-DOC Code Generator", version="%prog 1.0")
    p.description = "The ES-DOC meta-programming utility is a domain driven design tool designed to support the earth system documentation eco-system."
    p.add_option("-s",
                 action="store",
                 dest="schema_name",
                 type="choice",
                 choices=["cim"],
                 default="cim",
                 help="Target schema. [default = %default] [choices = cim]")
    p.add_option("-v",
                 action="store",
                 dest="schema_version",
                 type="string",
                 default="latest",
                 help="Target schema version. [default = %default]")
    p.add_option("-l",
                 action="store",
                 dest="language",
                 type="str",
                 help="Target programming language. [choices = c++, fortran, java, javascript, python]")
    p.add_option("-o",
                 action="store",
                 dest="output_dir",
                 type="string",
                 help="Target directory into which code will be generated.")

    return p.parse_args()[0]


# Get command line options.
options = _get_options()

# Get ontology schema.
ontology_schema = create_ontology_schema(options.schema_name, options.schema_version)

# Generate.
generate(ontology_schema, options.language, options.output_dir)

