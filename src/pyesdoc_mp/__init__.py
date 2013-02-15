"""
.. module:: pyesdoc_mp.generate.py
   :copyright: Copyright "Feb 7, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: pyesdoc_mp code generator.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

import optparse
import os

from pyesdoc_mp.generators.generator_options import GeneratorOptions
from pyesdoc_mp.utils.exception import ESDOCException
from pyesdoc_mp.utils.factory import (
    create_generators,
    create_ontology,
    create_ontology_schema
    )
from pyesdoc_mp.utils.validation import (
    validate_language,
    validate_ontology_schema,
    validate_output_dir
    )


# Package version identifier.
__version__ = '0.2'



def generate(ontology_schema, language, output_dir):
    """Generates code.

    :param ontology_schema: Ontology schema definition.
    :param language: Target programming language.
    :param output_dir: Target output directory.
    :type ontology_schema: dict
    :type language: str
    :type output_dir: str

    """
    print("-------------------------------------------------------------------")
    print("ES-DOC :: Welcome to the ES-DOC code generator")

    # Defensive programming.
    if can_generate(ontology_schema, language, output_dir):
        # Notify pre-generation.
        print("-------------------------------------------------------------------")
        print("ES-DOC :: GENERATION OPTION : schema = {0}".format(ontology_schema['name']))
        print("ES-DOC :: GENERATION OPTION : schema version = {0}".format(ontology_schema['version']))
        print("ES-DOC :: GENERATION OPTION : language = {0}".format(language))
        print("ES-DOC :: GENERATION OPTION : output directory = {0}".format(output_dir))
        
        # Initialise ontology.
        ontology = create_ontology(ontology_schema)        
        print("-------------------------------------------------------------------")
        print("ES-DOC :: ONTOLOGY = {0} (packages={1}, classes={2}, enums={3})".format(
            ontology, len(ontology.packages), len(ontology.classes), len(ontology.enums)))

        # Invoke generators.
        generators = create_generators(language)
        for generator_key in create_generators(language):
            print("-------------------------------------------------------------------")
            print("ES-DOC :: GENERATOR = {0} :: generation begins".format(generator_key))

            options = GeneratorOptions(generator_key, language, output_dir)
            generator = generators[generator_key]()
            generator.execute(ontology, options)
            
            print("ES-DOC :: GENERATOR = {0} :: generation complete".format(generator_key))

    print("-------------------------------------------------------------------")
    print("ES-DOC :: Thank you for using the ES-DOC code generator")
    print("-------------------------------------------------------------------")


def can_generate(ontology_schema, language, output_dir):
    """Verifies whether the generation options are in a state such that generation can occur.

    :param ontology_schema: Ontology schema definition.
    :param language: Target programming language.
    :param output_dir: Target output directory.
    :type ontology_schema: dict
    :type language: str
    :type output_dir: str
    :returns: True if generation can occur, False otherwise.
    :rtype: bool

    """
    # Validate.
    errors = validate_language(language)
    errors += validate_output_dir(output_dir)
    errors += validate_ontology_schema(ontology_schema)
    
    # Report errors.
    if errors:
        print("-------------------------------------------------------------------")
        print("ES-DOC :: INVALID GENERATOR OPTIONS !!!")
        for error in errors:
            print("ES-DOC :: GENERATOR OPTION ERROR :: {0}".format(error))

    return len(errors) == 0

