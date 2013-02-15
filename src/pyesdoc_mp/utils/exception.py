"""
.. module:: pyesdoc_mp.utils.exception
   :platform: Unix, Windows
   :synopsis: Default library exception class.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""



class ESDOCException(Exception):
    """Default library exception class.
    
    """

    def __init__(self, message):
        """Contructor.

        :param message: Exception message.

        :type message: str

        """
        self.message = message


    def __str__(self):
        """Returns a string representation.

        """
        return "ES-DOC CODE-GEN :: !!! EXCEPTION !!! : {0}".format(repr(self.message))
