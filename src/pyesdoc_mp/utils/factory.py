"""
.. module:: pyesdoc_mp.utils.factory
   :platform: Unix, Windows
   :synopsis: Encapsulates process of instantiating objects, i.e. generators, schemas and ontologies.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
from pyesdoc_mp.schemas import schemas as ontology_schemas



def _get_generators_for_python():
    """Returns set of supported python code generators.

    """
    from pyesdoc_mp.generators.python import (
        DecodingGenerator,
        RootGenerator,
        TypesGenerator,
        ValidationGenerator
        )

    return {
        'root' : RootGenerator,
        'types' : TypesGenerator,
        'decoding' : DecodingGenerator,
        'validation' : ValidationGenerator
    }


# Set of supported generators grouped by programming language.
_generators = {
    'python' : _get_generators_for_python
}


def create_generators(language):
    """Factory method to instantiate a set of generators filtered by programming language.

    :param language: A supported programming language.
    :type language: str
    :returns: A list of generators.
    :rtype: list

    """
    return {} if language not in _generators else _generators[language]()


def create_ontology_schema(name, version):
    """Factory method to instantiate an ontology schema instance.

    :param name: Schema name.
    :param version: Schema version.
    :type name: str
    :type version: str
    :returns: An ontology schema.
    :rtype: dict

    """
    for schema in ontology_schemas:
        if schema['name'].lower() == name.lower() and \
           schema['version'].lower() == version.lower():
            return schema
    return None


def create_ontology(schema):
    """Factory method to instantiate an ontology instance from a schema declaration.

    :param schema: An ontology schema declaration.
    :type schema: dict
    :returns: An ontology declaration.
    :rtype: pyesdoc_mp.ontology.Ontology

    """
    from pyesdoc_mp.ontology import (
        Class,
        Decoding,
        Enum,
        EnumMember,
        Ontology,
        Package,
        Property
        )

    o_packages = []
    for p_cfg in schema['packages']:
        # ... package classes
        p_classes = []
        for c_cfg in p_cfg['classes']:
            # ... class properties
            c_properties = []
            if 'properties' in c_cfg:
                for cp_cfg in c_cfg['properties']:
                    c_property = Property(cp_cfg[0], cp_cfg[3], cp_cfg[1], cp_cfg[2])
                    c_properties.append(c_property)

            # ... class constants
            c_constants = []
            if 'constants' in c_cfg:
                c_constants = c_cfg['constants']

            # ... class decodings
            c_decodings = []
            if 'decodings' in c_cfg:
                for d_cfg in c_cfg['decodings']:
                    c_decoding = cp_name = cp_decoding = cp_type = None
                    if len(d_cfg) == 2:
                        cp_name, cp_decoding = d_cfg
                    elif len(d_cfg) == 3:
                        cp_name, cp_decoding, cp_type = d_cfg
                    c_decoding = Decoding(cp_name, cp_decoding, cp_type)
                    c_decodings.append(c_decoding)

            # ... class
            c = Class(c_cfg['name'], c_cfg['base'], c_cfg['abstract'], c_cfg['doc'], c_properties, c_constants, c_decodings)
            p_classes.append(c)

        # ... package enums
        p_enums = []
        for e_cfg in p_cfg['enums']:
            # ... enum members
            e_members = []
            for em_cfg in e_cfg['members']:
                em_name = em_cfg[0]
                em_doc = em_cfg[1]
                e_members.append(EnumMember(em_name, em_doc))

            # ... enum
            p_enums.append(Enum(e_cfg['name'], e_cfg['is_open'], e_cfg['doc'], e_members))

        # ... package
        o_packages.append(Package(p_cfg['name'], p_cfg['doc'], p_classes, p_enums))

    return Ontology(schema['name'], schema['version'], schema['doc'], o_packages)