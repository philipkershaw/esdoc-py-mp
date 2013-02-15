"""
The cim v1.5 ontology - data package.
"""

# Module imports.
from pyesdoc_mp.schemas.cim.v1_5.data.classes import classes
from pyesdoc_mp.schemas.cim.v1_5.data.enums import enums


# Module exports.
__all__ = ["package"]


# Module provenance info.
__author__="markmorgan"
__copyright__ = "Copyright 2010, Insitut Pierre Simon Laplace - Prodiguer"
__date__ ="$Jun 28, 2010 2:52:22 PM$"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Sebastien Denvil"
__email__ = "sdipsl@ipsl.jussieu.fr"
__status__ = "Production"

# CIM v1.5 - data package.
package = {
    'name' : 'data',
    'doc' : 'TODO get package documentation',
    'classes' : classes,
    'enums' : enums,
}
