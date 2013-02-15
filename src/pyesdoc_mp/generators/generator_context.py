"""
.. module:: pyesdoc_mp.generators.generator_context
   :platform: Unix, Windows
   :synopsis: Encpasulates contextual information used by generators.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""



class GeneratorContext(object):
    """Encpasulates contextual information used by generators.

    :ivar ontology: Ontology being processed.
    :ivar options: Generation options.

    """
    def __init__(self, ontology, options):
        """Constructor.

        :param ontology: Ontology being processed.
        :param options: Generation options.
        :type ontology: pyesdoc_mp.ontology.Ontology
        :type options: pyesdoc_mp.GeneratorOptions

        """
        self.ontology = ontology
        self.options = options
        self.pkg = None
        self.cls = None
        self.enum = None
        

    @property
    def language(self):
        """Gets target programming language."""
        return self.options.language


    @property
    def generator_key(self):
        """Gets generator key."""
        return self.options.generator_key


    @property
    def output_dir(self):
        """Gets target output directory."""
        return self.options.output_dir


    def set_package(self, pkg):
        """Sets current package being processed.

        :param pkg: An ontology package being processed.
        :type pkg: pyesdoc_mp.ontology.package.Package

        """
        self.pkg = pkg
        self.cls = None
        self.enum = None


    def set_class(self, cls):
        """Sets current class type being processed.

        :param cls: A class type being processed.
        :type cls: pyesdoc_mp.ontology.class_.Class

        """
        self.pkg = cls.package
        self.cls = cls
        self.enum = None


    def set_enum(self, enum):
        """Sets current enumerated type being processed.

        :param enum: An enumerated type being processed.
        :type enum: pyesdoc_mp.ontology.enum.Enum

        """
        self.pkg = enum.package
        self.cls = None
        self.enum = enum
