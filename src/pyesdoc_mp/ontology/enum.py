"""
.. module:: pyesdoc_mp.ontology.enum
   :platform: Unix, Windows
   :synopsis: Represents an ontological enumerated type definition.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

class Enum(object):
    """Represents an enumeration, i.e. a constrained set of values.

    :ivar name: Enumeration name.
    :ivar is_open: Flag indicating whether members can be added to the enumeration or not.
    :ivar doc_string: Enumeration documentation string.
    :ivar members: Set of associated enumeration members.

    """
    def __init__(self, name, is_open, doc_string, members):
        """Constructor.

        :param name: Enumeration name.
        :param is_open: Flag indicating whether members can be added to the enumeration or not.
        :param doc_string: Enumeration documentation string.
        :param members: Set of associated enumeration members.
        :type name: str
        :type is_open: bool
        :type doc_string: str
        :type members: list

        """
        # Set relations.
        for m in members:
            m.enum = self

        # Set attributes.
        self.name = name
        self.is_open = is_open
        self.doc_string = doc_string if doc_string is not None else ''
        self.members = sorted(members, key=lambda m: m.name)
        self.package = None
        

    def __repr__(self):
        """String representation for debugging."""
        return self.name

