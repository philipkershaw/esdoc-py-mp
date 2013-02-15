"""
.. module:: pyesdoc_mp.ontology.property
   :platform: Unix, Windows
   :synopsis: Represents an ontological type property definition.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
from pyesdoc_mp.ontology.type import Type



class Property(object):
    """Represents a property within an ontology.

    :ivar name: Property name.
    :ivar doc_string: Property docuemtnation string.
    :ivar type_name: Property type name.
    :ivar cardinality: Type of relationship to associated class (i.e. 0.1 | 1.1 | 0.N | 1.N).

    """

    def __init__(self, name, doc_string, type_name, cardinality):
        """Constructor.

        :param name: Property name.
        :param doc_string: Property docuemtnation string.
        :param type_name: Property type name.
        :param cardinality: Type of relationship to associated class (i.e. 0.1 | 1.1 | 0.N | 1.N).
        :type name: str
        :type doc_string: str
        :type type_name: str
        :type cardinality: str

        """
        # Set attributes.
        self.cls = None
        self.decodings = []
        self.doc_string = doc_string if doc_string is not None else ''
        self.max_occurs = cardinality.split('.')[1]
        self.min_occurs = cardinality.split('.')[0]
        self.name = name
        self.type = Type(type_name)

        # Derived attributes.
        self.is_required = self.min_occurs != '0'
        self.is_iterative = self.max_occurs == 'N'


    def __repr__(self):
        """String representation for debugging."""
        return self.name
