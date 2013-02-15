"""
.. module:: pyesdoc_mp.ontology.package
   :platform: Unix, Windows
   :synopsis: Represents an ontological package definition.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

class Package(object):
    """Represents a package within an ontology.

    :ivar name: Package name.
    :ivar doc_string: Package documentation string.
    :ivar classes: Set of associated classes.
    :ivar enums: Set of associated enums.

    """

    def __init__(self, name, doc_string, classes, enums):
        """Constructor.

        :param name: Package name.
        :param doc_string: Package documentation string.
        :param classes: Set of associated classes.
        :param enums: Set of associated enums.
        :type name: str
        :type doc_string: str
        :type classes: list
        :type enums: list

        """
        # Set relations.
        for cls in classes:
            cls.package = self
        for enum in enums:
            enum.package = self

        # Set attributes.
        self.classes = sorted(classes, key=lambda c: c.name)
        self.doc_string = doc_string
        self.entities = []
        self.enums = sorted(enums, key=lambda e: e.name)
        self.external_types = []
        self.name = name
        self.properties = []
        self.types = []
        
        # Derive superset of entities.
        self.entities = sorted([c for c in classes if c.is_entity])

        # Derive superset of types.
        self.types = sorted(classes + enums, key=lambda t: t.name)

        # Derive superset of properties.
        for cls in self.classes:
            for prp in cls.properties:
                self.properties.append(prp)
        
        # Derive superset of external types.
        for prp in self.properties:
            if prp.type.is_complex and \
               prp.type.name_of_package != self.name and \
               prp.type not in self.external_types:
                self.external_types.append(prp.type)


    def __repr__(self):
        """String representation for debugging."""
        return self.name





