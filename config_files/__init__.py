"""
PennyStalker Configuration Package
Import all configuration classes for easy access
"""

from .DataSources import DataSources
from .CatalystKeywords import CatalystKeywords
from .CatalystTypes import CatalystTypes
from .CatalystRequirements import CatalystRequirements
from .DilutionKeywords import DilutionKeywords
from .FilingTypes import FilingTypes
from .ScoringWeights import ScoringWeights
from .ScoringThresholds import ScoringThresholds
from .TimeWindows import TimeWindows
from .ScanParameters import ScanParameters
from .Patterns import Patterns
from .helper_functions import (
    get_all_catalyst_keywords,
    get_all_dilution_keywords,
    is_dilution_filing,
    is_confirmation_filing
)

__all__ = [
    'DataSources',
    'CatalystKeywords',
    'CatalystTypes',
    'CatalystRequirements',
    'DilutionKeywords',
    'FilingTypes',
    'ScoringWeights',
    'ScoringThresholds',
    'TimeWindows',
    'ScanParameters',
    'Patterns',
    'get_all_catalyst_keywords',
    'get_all_dilution_keywords',
    'is_dilution_filing',
    'is_confirmation_filing',
]