"""
.. module:: pyesdoc_mp.generators.python.__init__.py
   :copyright: Copyright "Feb 7, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Package initialisor.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
from pyesdoc_mp.schemas.cim import schemas as cim_schemas


# Set of schemas supported 'out of the box'.
schemas = []
schemas.extend(cim_schemas)

