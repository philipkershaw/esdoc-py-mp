"""
.. module:: pyesdoc_mp.ontology.enum_member
   :platform: Unix, Windows
   :synopsis: Represents an ontological enumerated type member definition.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

class EnumMember(object):
    """Represents an enumeration member, i.e. a constrained value associated with an enumeration.

    :ivar name: Enumeration member name.
    :ivar name: Enumeration member documentation string.

    """
    def __init__(self, name, doc_string):
        """Constructor.

        :param name: Enumeration member name.
        :param doc_string: Enumeration member documentation string.
        :type name: str
        :type doc_string: str

        """
        # Set attributes.
        self.enum = None
        self.name = name
        self.doc_string = doc_string


    def __repr__(self):
        """String representation for debugging."""
        return self.name
