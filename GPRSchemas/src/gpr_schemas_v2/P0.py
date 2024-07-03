
import numpy as np

from nomad.metainfo import Package, MSection, Quantity, SubSection, MSection
from nomad.datamodel.data import Schema
from nomad.datamodel.metainfo.annotations import ELNAnnotation
from gpr_schemas_v2.base import Experiment, _GPR
from datetime import datetime

class Durations(Experiment):
    amplitude = Quantity(
        type=np.dtype('float64'),
        unit='degree',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity',
            defaultDisplayUnit='degree'
        ),
    )
    length = Quantity(
        type=np.dtype('float64'),
        unit='m',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity',
            defaultDisplayUnit='m'
        ),
    )
    zeroPoint = Quantity(
        type=np.dtype('float64'),
        unit='s',
        shape=['*'],
        a_eln=ELNAnnotation(
            component='NumberEditQuantity',
            defaultDisplayUnit='s'
        ),
    )
    reversePoint = Quantity(
        type=np.dtype('float64'),
        unit='s',
        shape=['*'],
        a_eln=ELNAnnotation(
            component='NumberEditQuantity',
            defaultDisplayUnit='s'
        ),
    )

class PeriodVsAmplitude(Experiment):
    length = Quantity(
        type=np.dtype('float64'),
        unit='m',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity',
            defaultDisplayUnit='m'
        ),
    )
    amplitude = Quantity(
        type=np.dtype('float64'),
        unit='degree',
        shape=['*'],
        a_eln=ELNAnnotation(
            component='NumberEditQuantity',
            defaultDisplayUnit='degree'
        ),
    )
    period = Quantity(
        type=np.dtype('float64'),
        unit='s',
        shape=['*'],
        a_eln=ELNAnnotation(
            component='NumberEditQuantity',
            defaultDisplayUnit='s'
        ),
    )    

class PeriodVsLength(Experiment):
    amplitude = Quantity(
        type=np.dtype('float64'),
        unit='degree',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity',
            defaultDisplayUnit='degree'
        ),
    )
    length = Quantity(
        type=np.dtype('float64'),
        unit='m',
        shape=['*'],
        a_eln=ELNAnnotation(
            component='NumberEditQuantity',
            defaultDisplayUnit='m'
        ),
    )
    period = Quantity(
        type=np.dtype('float64'),
        unit='s',
        shape=['*'],
        a_eln=ELNAnnotation(
            component='NumberEditQuantity',
            defaultDisplayUnit='s'
        ),
    )    
    
class _P0_Fadenpendel(_GPR):
    singlePeriod = SubSection(
        section=Durations,
        description='Single-period measurements at fixed amplitude and length',
    )
    tenPeriods = SubSection(
        section=Durations,
        description='10-period measurements at fixed amplitude and length',
    )
    periodVsAmplitude = SubSection(
        section=PeriodVsAmplitude,
        description='Period measurement at fixed length and varying amplitudes',
    )
    periodVsLength = SubSection(
        section=PeriodVsLength,
        description='Period measurement at fixed amplitude and varying lengths',
    )

    def _normalize(self, archive, logger):
        if not self.lab_name:
            self.lab_name = 'P0 -- Fadenpendel'
        if not self.lab_date:
            self.lab_date = datetime.today()
        if not self.singlePeriod:
            self.singlePeriod = Durations(notes='',zeroPoint=np.zeros(10), reversePoint=np.zeros(10),length=0,amplitude=0)
        if not self.tenPeriods:
            self.tenPeriods = Durations(notes='',zeroPoint=np.zeros(10), reversePoint=np.zeros(10),length=0,amplitude=0)
        if not self.periodVsAmplitude:
            self.periodVsAmplitude = PeriodVsAmplitude(notes='',period=np.zeros(10),length=0,amplitude=np.zeros(10))
        if not self.periodVsLength:
            self.periodVsLength = PeriodVsLength(notes='',period=np.zeros(10),length=np.zeros(10),amplitude=0)
