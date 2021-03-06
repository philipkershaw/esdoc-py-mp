"""
CIM v1.5 shared package classes.
"""
# Module exports.
__all__ = ["classes"]


# Module provenance info.
__author__="markmorgan"
__copyright__ = "Copyright 2010, Insitut Pierre Simon Laplace - Prodiguer"
__date__ ="$Jun 28, 2010 2:52:22 PM$"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Sebastien Denvil"
__email__ = "sdipsl@ipsl.jussieu.fr"
__status__ = "Production"


# --------------------------------------- #
# --------  Time related classes  ------- #
# --------------------------------------- #

def _calendar():
    """Creates and returns instance of calendar class."""
    return {
        'type' : 'class',
        'name' : 'calendar',
        'base' : None,
        'abstract' : True,
        'doc' : 'Describes a method of calculating a span of dates.',
        'properties' : [
            ('description', 'str', '0.1', 'Describes the finer details of the calendar, in case they are not-obvious.  For example, if an experiment has changing conditions within it (ie: 1% CO2 increase until 2100, then hold fixed for the remaining period of the  experment)'),
            ('length', 'int', '0.1', None),
            ('range', 'shared.date_range', '0.1', None),
        ],
        'decodings' : [
            ('description', 'child::cim:description'),
            ('length', 'child::cim:length'),
            ('range', 'child::cim:range/cim:closedDateRange', 'shared.closed_date_range'),
            ('range', 'child::cim:range/cim:openDateRange', 'shared.open_date_range'),
        ]
    }


def _closed_date_range():
    """Creates and returns instance of closed_date_range class."""
    return {
        'type' : 'class',
        'name' : 'closed_date_range',
        'base' : 'shared.date_range',
        'abstract' : False,
        'doc' : 'A date range with specified start and end points.',
        'properties' : [
            ('end', 'datetime', '0.1', 'End date is optional becuase the length of a ClosedDateRange can be calculated from the StartDate plus the Duration element.'),
            ('start', 'datetime', '1.1', None),
        ],
        'decodings' : [
            ('end', 'child::cim:endDate'),
            ('start', 'child::cim:startDate'),
        ]
    }


def _daily_360():
    """Creates and returns instance of daily_360 class."""
    return {
        'type' : 'class',
        'name' : 'daily_360',
        'base' : 'shared.calendar',
        'abstract' : False,
        'doc' : None,
        'properties' : [ ],
        'decodings' : [ ]
    }


def _date_range():
    """Creates and returns instance of date_range class."""
    return {
        'type' : 'class',
        'name' : 'date_range',
        'base' : None,
        'abstract' : True,
        'doc' : None,
        'properties' : [
            ('duration', 'str', '0.1', None),
        ],
        'decodings' : [
            ('duration', 'child::cim:duration'),
        ]
    }


def _open_date_range():
    """Creates and returns instance of open_date_range class."""
    return {
        'type' : 'class',
        'name' : 'open_date_range',
        'base' : 'shared.date_range',
        'abstract' : False,
        'doc' : 'A date range without a specified start and/or end point.',
        'properties' : [
            ('end', 'datetime', '0.1', None),
            ('start', 'datetime', '0.1', None),
        ],
        'decodings' : [
            ('end', 'child::cim:endDate'),
            ('start', 'child::cim:startDate'),
        ]
    }

# --------------------------------------- #
# --------  CIM related classes  -------- #
# --------------------------------------- #

def _cim_document_relationship():
    """Creates and returns instance of cim_document_relationship class."""
    return {
        'type' : 'class',
        'name' : 'cim_document_relationship',
        'base' : 'shared.cim_relationship',
        'abstract' : False,
        'doc' : 'Contains the set of relationships supported by a Document.',
        'properties' : [
            ('target', 'shared.cim_document_relationship_target', '1.1', None),
            ('type', 'shared.cim_document_relationship_type', '1.1', None),
        ],
        'decodings' : [
            ('description', 'child::cim:description'),
            ('direction', 'self::cim:documentRelationship/@direction'),
            ('type', 'self::cim:documentRelationship/@type'),
            ('target', 'child::cim:target'),
        ]
    }


def _cim_document_relationship_target():
    """Creates and returns instance of cim_document_relationship_target class."""
    return {
        'type' : 'class',
        'name' : 'cim_document_relationship_target',
        'base' : None,
        'abstract' : False,
        'doc' : None,
        'properties' : [
            ('reference', 'shared.cim_reference', '0.1', None),
            ('document', 'shared.cim_document_type', '0.1', None),
        ],
        'decodings' : [
            ('reference', 'child::cim:reference'),
        ]
    }


def _cim_info():
    """Creates and returns instance of cim_info class."""
    return {
        'type' : 'class',
        'name' : 'cim_info',
        'base' : None,
        'abstract' : False,
        'doc' : 'Encapsulates common cim information.',
        'properties' : [
            ('author', 'shared.responsible_party', '0.1', 'Universally identifies the CIM instance'),
            ('create_date', 'datetime', '1.1', 'The date the instance was created'),
            ('external_ids', 'shared.standard_name', '0.N', 'A non-CIM (non-GUID) id used to reference the element in question.'),
            ('genealogy', 'shared.cim_genealogy', '0.1', 'Specifies the relationship of this document with another document. Various relationship types (depending on the type of document; ie: simulation, component, etc.) are supported.'),
            ('id', 'uuid', '1.1', 'Universally identifies the instance.'),
            ('language', 'str', '1.1', 'Language with which instance is associated with.'),
            ('metadata_id', 'uri', '0.1', None),
            ('metadata_version', 'str', '0.1', None),
            ('project', 'str', '1.1', 'Name of project with which instance is associated with.'),
            ('source', 'str', '1.1', 'The source application that created the instance.'),
            ('status', 'shared.document_status_type', '0.1', None),
            ('version', 'str', '1.1', 'Universally identifies the instance version.'),
            ('type_info', 'shared.cim_type_info', '0.1', 'Type information used to a priori identify type.'),
        ],
        'decodings' : [
            ('author', 'child::cim:documentAuthor'),
            ('create_date', 'child::cim:documentCreationDate'),
            ('external_ids', 'child::cim:externalID'),
            ('genealogy', 'child::cim:documentGenealogy'),
            ('id', 'child::cim:documentID'),
            ('version', 'child::cim:documentVersion'),
        ]
    }


def _cim_type_info():
    """Creates and returns instance of cim_type_info class."""
    return {
        'type' : 'class',
        'name' : 'cim_type_info',
        'base' : None,
        'abstract' : False,
        'doc' : 'Encapsulates cim type information.',
        'properties' : [
            ('schema', 'str', '1.1', 'Schema version.'),
            ('package', 'str', '1.1', 'Package name.'),
            ('type', 'str', '1.1', 'Type name.'),
            ('type_display_name', 'str', '1.1', 'Type display name.'),
        ],
        'decodings' : [
        ]
    }


def _cim_genealogy():
    """Creates and returns instance of cim_genealogy class."""
    return {
        'type' : 'class',
            'name' : 'cim_genealogy',
        'base' : None,
        'abstract' : False,
        'doc' : 'A record of a document\'s history. A genealogy element contains a textual description and a set of relationships. Each relationship has a type and a reference to some target. There are different relationships for different document types.',
        'properties' : [
            ('relationships', 'shared.cim_relationship', '0.N', None),
        ],
        'decodings' : [
            ('relationships', 'child::cim:relationship/cim:documentRelationship', 'shared.cim_document_relationship'),
        ]
    }


def _cim_reference():
    """Creates and returns instance of reference class."""
    return {
        'type' : 'class',
        'name' : 'cim_reference',
        'base' : None,
        'abstract' : False,
        'doc' : 'A reference to another cim entity',
        'properties' : [
            ('changes', 'shared.change', '0.N', 'An optional description of how the item being referenced has been modified.  This is particularly useful for dealing with Ensembles (a set of simulations where something about each simulation has changed) or Conformances.'),
            ('description', 'str', '0.1', 'A description of the element being referenced, in the context of the current class.'),
            ('external_id', 'str', '0.1', 'A non-CIM (non-GUID) id used to reference the element in question.'),
            ('id', 'uuid', '0.1', 'The ID of the element being referenced.'),
            ('name', 'str', '0.1', 'The name of the element being referenced.'),
            ('type', 'str', '0.1', 'The type of the element being referenced.'),
            ('version', 'str', '0.1', 'The version of the element being referenced.'),
        ],
        'decodings' : [
            ('changes', 'child::cim:change'),
            ('description', 'child::cim:description'),
            ('external_id', 'child::cim:externalID'),
            ('id', 'child::cim:id'),
            ('name', 'child::cim:name'),
            ('type', 'child::cim:type'),
            ('version', 'child::cim:version'),
        ]
    }


def _cim_relationship():
    """Creates and returns instance of relationship class."""
    return {
        'type' : 'class',
        'name' : 'cim_relationship',
        'base' : None,
        'abstract' : True,
        'doc' : 'A record of a relationship between one document and another. This class is abstract; specific document types must specialise this class for their relationshipTypes to be included in a document\'s genealogy.',
        'properties' : [
            ('description', 'str', '0.1', None),
            ('direction', 'shared.cim_relationship_direction_type', '1.1', None),
        ],
        'decodings' : [
        ]
    }

# --------------------------------------- #
# --------  Other classes        -------- #
# --------------------------------------- #

def _change():
    """Creates and returns instance of change class."""
    return {
        'type' : 'class',
        'name' : 'change',
        'base' : None,
        'abstract' : False,
        'doc' : 'A description of [a set of] changes applied at a particular time, by a particular party, to a particular unit of metadata.',
        'properties' : [
            ('author', 'shared.responsible_party', '0.1', 'The person that made the change.'),
            ('date', 'datetime', '0.1', 'The date the change was implemented.'),
            ('description', 'str', '0.1', None),
            ('details', 'shared.change_property', '1.N', None),
            ('name', 'str', '0.1', 'A mnemonic for describing a particular change.'),
            ('type', 'shared.change_property_type', '0.1', None),
        ],
        'decodings' : [
            ('author', 'child::cim:changeAuthor'),
            ('date', 'child::cim:changeDate'),
            ('description', 'child::cim:description'),
            ('details', 'child::cim:detail'),
            ('name', 'child::cim:name'),
            ('type', 'self::cim:change/@type'),
        ]
    }
    

def _change_property():
    """Creates and returns instance of change class."""
    return {
        'type' : 'class',
        'name' : 'change_property',
        'base' : 'shared.property',
        'abstract' : False,
        'doc' : 'A description of a single change applied to a single target.  Every ChangeProperty has a description, and may also have a name from a controlled vocabulary and a value.',
        'properties' : [
            ('description', 'str', '0.1', 'A text description of the change.  May be used in addition to, or instead of, the more formal description provided by the "value" attribute.'),
            ('id', 'str', '0.1', None),
        ],
        'decodings' : [
            ('description', 'child::cim:description'),
            ('id', 'child::cim:id'),
        ]
    }


def _citation():
    """Creates and returns instance of citation class."""
    return {
        'type' : 'class',
        'name' : 'citation',
        'base' : None,
        'abstract' : False,
        'doc' : 'An academic reference to published work.',
        'properties' : [
            ('alternative_title', 'str', '0.1', None),
            ('collective_title', 'str', '0.1', None),
            ('location', 'str', '0.1', None),
            ('date', 'datetime', '0.1', None),
            ('date_type', 'str', '0.1', None),
            ('organisation', 'str', '0.1', None),
            ('reference', 'shared.cim_reference', '0.1', None),
            ('role', 'str', '0.1', None),
            ('title', 'str', '0.1', None),
            ('type', 'str', '0.1', None),
        ],
        'decodings' : [
            ('alternative_title', 'child::gmd:alternateTitle/gco:CharacterString'),
            ('collective_title', 'gmd:collectiveTitle/gco:CharacterString'),
            ('date', 'child::gmd:date/gmd:CI_Date/gmd:date/gco:Date'),
            ('date_type', 'child::gmd:date/gmd:CI_Date/gmd:dateType/gmd:CI_DateTypeCode/@codeListValue'),
            ('location', 'child::gmd:otherCitationDetails/gco:CharacterString'),
            ('title', 'child::gmd:title/gco:CharacterString'),
            ('type', 'child::gmd:presentationForm/gmd:CI_PresentationFormCode/@codeListValue'),
        ]
    }


def _compiler():
    """Creates and returns instance of compiler class."""
    return {
        'type' : 'class',
        'name' : 'compiler',
        'base' : None,
        'abstract' : False,
        'doc' : 'A description of a compiler used on a particular platform.',
        'properties' : [
            ('environment_variables', 'str', '0.1', 'The set of environment_variables used during compilation (recorded here as a single string rather than separate elements)'),
            ('language', 'str', '0.1', None),
            ('name', 'str', '1.1', None),
            ('options', 'str', '0.1', 'The set of options used during compilation (recorded here as a single string rather than separate elements)'),
            ('type', 'shared.compiler_type', '0.1', None),
            ('version', 'str', '1.1', None),
        ],
        'decodings' : [
            ('environment_variables', 'child::cim:compilerEnvironmentVariables'),
            ('language', 'child::cim:compilerLanguage'),
            ('name', 'child::cim:compilerName'),
            ('options', 'child::cim:compilerOptions'),
            ('type', 'child::cim:compilerType'),
            ('version', 'child::cim:compilerVersion'),
        ]
    }


def _data_source():
    """Creates and returns instance of data_source class."""
    return {
        'type' : 'class',
        'name' : 'data_source',
        'base' : None,
        'abstract' : True,
        'doc' : 'A DataSource can be realised by either a DataObject (file), a DataContent (variable), a Component (model), or a ComponentProperty (variable); all of those can supply data.',
        'properties' : [
            ('purpose', 'shared.data_purpose', '0.1', None),
        ],
        'decodings' : [
            
        ]
    }


def _license():
    """Creates and returns instance of license class."""
    return {
        'type' : 'class',
        'name' : 'license',
        'base' : None,
        'abstract' : False,
        'doc' : 'A description of a license restricting access to a unit of data or software',
        'properties' : [
            ('name', 'str', '0.1', 'The name that the license goes by (ie: "GPL")'),
            ('contact', 'str', '0.1', 'The point of contact for access to this artifact; may be either a person or an institution.'),
            ('description', 'str', '0.1', 'A textual description of the license; might be the full text of the license, more likely to be a brief summary'),
            ('is_unrestricted', 'str', '0.1', 'If unrestricted="true" then the artifact can be downloaded with no restrictions (ie: there are no administrative steps for the user to deal with; code or data can be downloaded and used directly).'),
        ],
        'decodings' : [

        ]
    }


def _machine():
    """Creates and returns instance of machine class."""
    return {
        'type' : 'class',
        'name' : 'machine',
        'base' : None,
        'abstract' : False,
        'doc' : 'A description of a machine used by a particular platform',
        'properties' : [
            ('cores_per_processor', 'int', '0.1', None),
            ('description', 'str', '0.1', None),
            ('interconnect', 'shared.interconnect_type', '0.1', None),
            ('name', 'str', '1.1', None),
            ('libraries', 'str', '0.N', 'The libraries residing on this machine.'),
            ('location', 'str', '0.1', None),
            ('maximum_processors', 'int', '0.1', None),
            ('operating_system', 'shared.operating_system_type', '0.1', None),
            ('system', 'str', '0.1', None),
            ('type', 'shared.machine_type', '0.1', None),
            ('vendor', 'shared.machine_vendor_type', '0.1', None),
            ('processor_type', 'shared.processor_type', '0.1', None),
        ],
        'decodings' : [
            ('cores_per_processor', 'child::cim:machineCoresPerProcessor'),
            ('description', 'child::cim:machineDescription'),
            ('interconnect', 'child::cim:machineInterconnect/@value'),
            ('name', 'child::cim:machineName'),
            ('libraries', 'child::cim:machineLibrary'),
            ('location', 'child::cim:machineLocation'),
            ('maximum_processors', 'child::cim:machineMaximumProcessors'),
            ('operating_system', 'child::cim:machineOperatingSystem/@value'),
            ('system', 'child::cim:machineSystem'),
            ('type', '@machineType'),
            ('vendor', 'child::cim:machineVendor/@value'),
            ('processor_type', 'child::cim:machineProcessorType/@value'),
        ]
    }


def _machine_compiler_unit():
    """Creates and returns instance of machine_compiler_unit class."""
    return {
        'type' : 'class',
        'name' : 'machine_compiler_unit',
        'base' : None,
        'abstract' : False,
        'doc' : 'Associates a machine with a [set of] compilers.  This is a separate class in case a platform needs to specify more than one machine/compiler pair.',
        'properties' : [
            ('compilers', 'shared.compiler', '0.N', None),
            ('machine', 'shared.machine', '1.1', None),
        ],
        'decodings' : [
            ('compilers', 'child::cim:compiler'),
            ('machine', 'child::cim:machine'),
        ]
    }


def _perpetual_period():
    """Creates and returns instance of perpetual_period class."""
    return {
        'type' : 'class',
        'name' : 'perpetual_period',
        'base' : 'shared.calendar',
        'abstract' : False,
        'doc' : None,
        'properties' : [ ],
        'decodings' : [ ]
    }


def _platform():
    """Creates and returns instance of platform class."""
    return {
        'type' : 'class',
        'name' : 'platform',
        'base' : None,
        'abstract' : False,
        'doc' : 'A platform is a description of resources used to deploy a component/simulation.  A platform pairs a machine with a (set of) compilers.  There is also a point of contact for the platform.',
        'properties' : [
            ('cim_info', 'shared.cim_info', '1.1', None),
            ('contacts', 'shared.responsible_party', '0.N', None),
            ('description', 'str', '0.1', None),
            ('long_name', 'str', '0.1', None),
            ('short_name', 'str', '1.1', None),
            ('units', 'shared.machine_compiler_unit', '1.N', None),
        ],
        'decodings' : [
            ('cim_info', 'self::cim:platform'),
            ('contacts', 'child::cim:contact'),
            ('description', 'child::cim:description'),
            ('long_name', 'child::cim:longName'),
            ('short_name', 'child::cim:shortName'),
            ('units', 'child::cim:unit'),
        ]
    }
    

def _property():
    """Creates and returns instance of property class."""
    return {
        'type' : 'class',
        'name' : 'property',
        'base' : None,
        'abstract' : False,
        'doc' : 'A simple name/value pair representing a property of some entity or other',
        'properties' : [
            ('name', 'str', '0.1', None),
            ('value', 'str', '0.1', None),
        ],
        'decodings' : [
            ('name', 'child::cim:name'),
            ('value', 'child::cim:value'),
        ]
    }


def _real_calendar():
    """Creates and returns instance of real_calendar class."""
    return {
        'type' : 'class',
        'name' : 'real_calendar',
        'base' : 'shared.calendar',
        'abstract' : False,
        'doc' : None,
        'properties' : [ ],
        'decodings' : [ ]
    }


def _responsible_party():
    """Creates and returns instance of responsible_party class."""
    return {
        'type' : 'class',
        'name' : 'responsible_party',
        'base' : None,
        'abstract' : False,
        'doc' : 'A person/organsiation responsible for some aspect of a climate science artefact',
        'properties' : [
            ('abbreviation', 'str', '0.1', None),
            ('contact_info', 'shared.responsible_party_contact_info', '1.1', None),
            ('individual_name', 'str', '0.1', None),
            ('organisation_name', 'str', '0.1', None),
            ('role', 'str', '0.1', None),
        ],
        'decodings' : [
            ('abbreviation', 'child::cim:abbreviation'),
            ('contact_info', 'child::gmd:contactInfo/gmd:CI_Contact'),
            ('individual_name', 'child::gmd:individualName/gco:CharacterString'),
            ('organisation_name', 'child::gmd:organisationName/gco:CharacterString'),
            ('role', 'gmd:role/gmd:CI_RoleCode/@codeListValue'),
        ]
    }


def _responsible_party_contact_info():
    """Creates and returns instance of responsible_party_contact_info class."""
    return {
        'type' : 'class',
        'name' : 'responsible_party_contact_info',
        'base' : None,
        'abstract' : False,
        'doc' : 'Maps gmd:contactInfo element.',
        'properties' : [
            ('address', 'str', '0.1', None),
            ('email', 'str', '0.1', None),
            ('url', 'str', '0.1', None),
        ],
        'decodings' : [
            ('address', 'child::gmd:address/gmd:CI_Address/gmd:deliveryPoint/gco:CharacterString'),
            ('email', 'child::gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString'),
            ('url', 'child::gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage/gmd:URL'),
        ]
    }


def _standard():
    """Creates and returns instance of standard class."""
    return {
        'type' : 'class',
        'name' : 'standard',
        'base' : None,
        'abstract' : False,
        'doc' : 'Describes a name given to an entity from a recognised standard.  The CIM records the standard and the name.  For example, the standard might be CF and the name might be atmospheric_pressure.',
        'properties' : [
            ('name', 'str', '1.1', 'The name of the standard'),
            ('version', 'str', '0.1', 'The version of the standard'),
            ('description', 'str', '0.1', 'The version of the standard'),

        ],
        'decodings' : [
            ('name', 'child::cim:name'),
            ('version', 'child::cim:version'),
            ('description', 'child::cim:description'),
        ]
    }


def _standard_name():
    """Creates and returns instance of standard_name class."""
    return {
        'type' : 'class',
        'name' : 'standard_name',
        'base' : None,
        'abstract' : False,
        'doc' : 'Describes a name given to an entity from a recognised standard.  The CIM records the standard and the name.  For example, the standard might be CF and the name might be atmospheric_pressure.',
        'properties' : [
            ('is_open', 'bool', '1.1', None),
            ('value', 'str', '1.1', None),
            ('standards', 'shared.standard', '0.N', 'Details of the standard being used.'),
        ],
        'decodings' : [
            ('is_open', '@open'),
            ('value', '@value'),
            ('standards', 'child::cim:standard'),
        ]
    }


# Set of package classes.
classes = [
        _calendar(),
        _cim_document_relationship(),
        _cim_document_relationship_target(),
        _cim_genealogy(),
        _cim_info(),
        _cim_reference(),
        _cim_relationship(),
        _cim_type_info(),
        _change(),
        _change_property(),
        _citation(),
        _closed_date_range(),
        _compiler(),
        _daily_360(),
        _data_source(),
        _date_range(),
        _license(),
        _machine(),
        _machine_compiler_unit(),
        _open_date_range(),
        _perpetual_period(),
        _platform(),
        _property(),
        _real_calendar(),
        _responsible_party(),
        _responsible_party_contact_info(),
        _standard(),
        _standard_name(),
]

