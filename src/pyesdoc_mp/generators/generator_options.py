"""
.. module:: pyesdoc_mp.generators.generator_options
   :platform: Unix, Windows
   :synopsis: Encapsulates set of generator options.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""



class GeneratorOptions(object):
    """Encapsulates set of generator options.

    :ivar generator_key: Key assigned to generator.
    :ivar language: Target code generation programming language.
    :ivar output_dir: Directory to which output will be generated.

    """
    def __init__(self, generator_key, language, output_dir):
        """Constructor.

        :param generator_key: Key assigned to generator.
        :param language: Target code generation programming language.
        :param output_dir: Directory to which output will be generated.
        :type generator_key: str
        :type language: str
        :type output_dir: str

        """
        self.generator_key = generator_key
        self.language = str(language).lower()
        self.output_dir = str(output_dir)
        