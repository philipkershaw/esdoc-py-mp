"""
.. module:: pyesdoc_mp.schemas.cim.__init__.py
   :copyright: Copyright "Feb 7, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Sub-package initializer.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
from pyesdoc_mp.schemas.cim.v1_5 import schema as v1_5



# Set of supported Metafor CIM schemas.
schemas = [
    v1_5
]

