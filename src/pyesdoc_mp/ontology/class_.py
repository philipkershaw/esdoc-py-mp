"""
.. module:: pyesdoc_mp.ontology.class
   :platform: Unix, Windows
   :synopsis: Represents an ontological class definition.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

class Class(object):
    """Represents an ontological class definition.

    :ivar name: Class name.
    :ivar base: Base class used in object hierarchies.
    :ivar is_abstract: Flag indicating whether this is an abstract class or not.
    :ivar doc_string: Class documentation string.
    :ivar properties: Set of associated properties.
    :ivar constants: Set of associated property constants.
    :ivar decodings: Set of associated property decodings.

    """

    def __init__(self, name, base, is_abstract, doc_string, properties, constants, decodings):
        """Constructor.

        :param name: Class name.
        :param base: Base class used in object hierarchies.
        :param is_abstract: Flag indicating whether this is an abstract class or not.
        :param doc_string: Class documentation string.
        :param properties: Set of associated properties.
        :param constants: Set of associated property constants.
        :param decodings: Set of associated property decodings.
        :type name: str
        :type base: str
        :type is_abstract: bool
        :type doc_string: str
        :type properties: list
        :type constants: list
        :type decodings: list
        
        """
        # Set relations.
        for prp in properties:
            prp.cls = self        

        # Set attributes.
        self.__all_decodings = None
        self.__all_properties = None
        self.base = base
        self.circular_imports = []
        self.constants = constants
        self.decodings = sorted(decodings, key=lambda dc: dc.property_name)
        self.doc_string = doc_string if doc_string is not None else ''
        self.imports = []
        self.is_abstract = is_abstract
        self.is_entity = False
        self.name = name
        self.properties = sorted(properties, key=lambda p: p.name)
        self.package = None
        
        # Set is entity flag.
        self.is_entity = is_abstract == False and self.has_property('cim_info')

        
    def __repr__(self):
        """String representation for debugging."""
        return self.name


    @property
    def all_constants(self):
        """Gets all associated constants including those of base class (sorted by name)."""
        # JIT instantiation.
        if self.__all_constants is None:
            self.__all_constants = list(self.constants)
            if self.base is not None:
                self.__all_constants += self.base.all_constants

        return self.__all_constants


    @property
    def all_properties(self):
        """Gets all associated properties including those of base class (sorted by name)."""
        # JIT instantiation.
        if self.__all_properties is None:
            self.__all_properties = list(self.properties)
            if self.base is not None:
                self.__all_properties += self.base.all_properties
            self.__all_properties = sorted(self.__all_properties, key=lambda p: p.name)

        return self.__all_properties


    @property
    def all_decodings(self):
        """Gets class plus base class decodings."""
        # JIT instantiation.
        if self.__all_decodings is None:
            self.__all_decodings = list(self.decodings)
            if self.base is not None:
                self.__all_decodings += self.base.all_decodings
                
        return self.__all_decodings


    def get_property_decodings(self, prp):
        """Returns set of property decodings.

        :param prp: A property being processed.
        :type prp: pyesdoc_mp.decoding.Decodings

        """
        result = []
        for dc in [dc for dc in self.all_decodings if dc.property_name == prp.name]:
            result.append(dc)
        return result


    def has_property(self, name):
        """Gets flag indicating whether this class has a property with same name.

        :param name: Name of a property potentially supported by this class.
        :type name: str

        """
        for prp in self.properties:
            if prp.name == name:
                return True
        return False


    def get_property(self, name):
        """Gets associated property either from self or from base.

        :param name: Name of a property.
        :type name: str

        """
        # Return from self.
        for prp in self.properties:
            if prp.name == name:
                return prp

        # Return from base.
        if self.base is not None:
            return self.base.get_property(name)

        # Unsupported.
        return None
        