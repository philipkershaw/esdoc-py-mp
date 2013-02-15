"""
CIM v1.5 quality package enums.
"""
# Module exports.
__all__ = ["enums"]


# Module provenance info.
__author__="markmorgan"
__copyright__ = "Copyright 2010, Insitut Pierre Simon Laplace - Prodiguer"
__date__ ="$Jun 28, 2010 2:52:22 PM$"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Sebastien Denvil"
__email__ = "sdipsl@ipsl.jussieu.fr"
__status__ = "Production"



def _cim_feature_type():
    """Creates and returns instance of cim_feature_type enum."""
    return {
        'name' : 'cim_feature_type',
        'is_open' : False,
        'doc' : None,
        'members' : [
            ('file', None),
            ('diagnostic', None),
        ],
    }

    
def _cim_result_type():
    """Creates and returns instance of cim_result_type enum."""
    return {
        'name' : 'cim_result_type',
        'is_open' : False,
        'doc' : None,
        'members' : [
            ('plot', None),
            ('document', None),
            ('logfile', None),
        ],
    }


def _cim_scope_code_type():
    """Creates and returns instance of cim_scope_code_type enum."""
    return {
        'name' : 'cim_scope_code_type',
        'is_open' : False,
        'doc' : 'This would cover quality issues with the CIM itself',
        'members' : [
            ('dataset', None),
            ('software', None),
            ('service', None),
            ('model', None),
            ('modelComponent', None),
            ('simulation', None),
            ('experiment', None),
            ('numericalRequirement', None),
            ('ensemble', None),
            ('file', None),
        ],
    }


def _quality_issue_type():
    """Creates and returns instance of quality_issue_type enum."""
    return {
        'name' : 'quality_issue_type',
        'is_open' : False,
        'doc' : None,
        'members' : [
            ('metadata', None),
            ('data_format', None),
            ('data_content', None),
            ('data_indexing', None),
            ('science', None),
        ],
    }


def _quality_severity_type():
    """Creates and returns instance of quality_severity_type enum."""
    return {
        'name' : 'quality_severity_type',
        'is_open' : False,
        'doc' : None,
        'members' : [
            ('cosmetic', None),
            ('minor', None),
            ('major', None),
        ],
    }


def _quality_status_type():
    """Creates and returns instance of quality_status_type enum."""
    return {
        'name' : 'quality_status_type',
        'is_open' : False,
        'doc' : None,
        'members' : [
            ('reported', None),
            ('confirmed', None),
            ('partially_resolved', None),
            ('resolved', None),
        ],
    }

    
# Set of package enums.
enums = [
    _cim_feature_type(),
    _cim_result_type(),
    _cim_scope_code_type(),
    _quality_issue_type(),
    _quality_severity_type(),
    _quality_status_type()
]

