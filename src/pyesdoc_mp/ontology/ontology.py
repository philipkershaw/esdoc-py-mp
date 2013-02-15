"""
.. module:: pyesdoc_mp.ontology.ontology
   :platform: Unix, Windows
   :synopsis: Represents an ontology definition.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
from operator import add
from functools import reduce

from pyesdoc_mp.ontology.class_ import Class



class Ontology(object):
    """Represents an ontology, i.e. a set of classes organised into packages.

    :ivar name: Ontology name.
    :ivar version: Ontology version.
    :ivar doc_string: Ontology documentation string.
    :ivar packages: Set of associated packages.

    """

    def __init__(self, name, version, doc_string, packages):
        """Constructor.

        :param name: Ontology name.
        :param version: Ontology version.
        :param doc_string: Ontology documentation string.
        :param packages: Set of associated packages.
        :type name: str
        :type version: str
        :type doc_string: str
        :type packages: list

        """
        # Set relations.
        for pkg in packages:
            pkg.ontology = self

        # Set attributes.
        self.name = name
        self.version = version
        self.doc_string = doc_string
        self.packages = sorted(packages, key=lambda p: p.name)

        # Set supersets.
        self.classes = reduce(add, map(lambda p : p.classes, packages))
        self.enums = reduce(add, map(lambda p : p.enums, packages))
        self.enum_members = reduce(add, map(lambda e : e.members, self.enums))
        self.entities = reduce(add, map(lambda p : p.entities, packages))
        self.properties = reduce(add, map(lambda c : c.properties, self.classes))
        self.property_types = map(lambda p : p.type, self.properties)
        self.types = sorted(self.classes + self.enums)

        # Set base classes.
        for c in [c for c in self.classes if c.base is not None]:
            t = self.get_type(c.base)
            if t is not None:
                c.base = t

        # Set property type is_class flag.
        for pt in [pt for pt in self.property_types if pt.is_complex]:
            t = self.get_type(pt.name)
            if t is not None:
                pt.is_class = isinstance(t, Class)

        # Set class imports.
        def append_to_class_imports(cls, package, type):
            if package != cls.package.name or \
               type != cls.name and \
               (package, type) not in cls.imports:
                cls.imports.append((package, type))
        
        for cls in self.classes:
            if cls.base is not None:
                package = cls.base.package.name
                type = cls.base.name
                append_to_class_imports(cls, package, type)

            for prp in [p for p in cls.properties if p.type.is_complex]:
                package = prp.type.name_of_package
                type = prp.type.name_of_type
                append_to_class_imports(cls, package, type)

        # Set class circular imports.
        for cls in self.classes:
            cls_import = (cls.package.name, cls.name)
            for prp in [p for p in cls.properties if p.type.is_class]:
                prp_type = self.get_type(prp.type.name)
                if cls_import in prp_type.imports:
                    prp_type.imports.remove(cls_import)
                    prp_type.circular_imports.append(cls_import)
    

    def __repr__(self):
        """String representation for debugging."""
        return self.name + ' v' + self.version


    def get_type(self, name):
        """Returns type with matching name.

        :param name: Fully qualified name of target type.
        :type name: str

        """
        pkg_name = name.split('.')[0]
        type_name = name.split('.')[1]
        for t in self.types:
            if t.package.name == pkg_name and t.name == type_name:
                return t
        return None
            