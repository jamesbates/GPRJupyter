
import numpy as np

from nomad.metainfo import Package, MSection, Quantity, SubSection, MSection
from nomad.datamodel.data import Schema
from nomad.datamodel.metainfo.annotations import ELNAnnotation
from gpr_schemas_v3.base import Experiment, _GPR
from datetime import datetime


class Durations(MSection):
    period = Quantity(
        type=np.dtype('float64'),
        unit='s',
        shape=['*'],
        a_eln=ELNAnnotation(
            component='NumberEditQuantity',
            defaultDisplayUnit='s'
        ),
    )

class SinglePeriods(Experiment):
    zeroPoint6 = SubSection(
        section=Durations,
        description='single-period measurement at zero point'
    )
    reversePoint6 = SubSection(
        section=Durations,
        description='single-period measurement at reverse point'
    )
    zeroPoint120 = SubSection(
        section=Durations,
        description='single-period (120) measurement at zero point'
    )
    errPeriodA = Quantity(
        type=np.dtype('float64'),
        a_eln=ELNAnnotation(
            component='NumberEditQuantity'
        ),
    )
    errPeriodB = Quantity(
        type=np.dtype('float64'),
        unit='s',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity',
            defaultDisplayUnit='s'
        ),
    )


class PeriodVsAmplitude(Experiment):
    amplitude = Quantity(
        type=np.dtype('float64'),
        unit='degree',
        shape=['*'],
        a_eln=ELNAnnotation(
            component='NumberEditQuantity',
            defaultDisplayUnit='degree'
        ),
    )
    errAmplitude = Quantity(
        type=np.dtype('float64'),
        unit='degree',
        shape=['*'],
        a_eln=ELNAnnotation(
            component='NumberEditQuantity',
            defaultDisplayUnit='degree'
        ),
    )
    fivePeriods = SubSection(
        section=Durations,
        description='5-period vs amplitude',
        repeats=True
    )    
    errPeriodA = Quantity(
        type=np.dtype('float64'),
        a_eln=ELNAnnotation(
            component='NumberEditQuantity'
        ),
    )
    errPeriodB = Quantity(
        type=np.dtype('float64'),
        unit='s',
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
    lengthOffset = Quantity(
        type=np.dtype('float64'),
        unit='m',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity',
            defaultDisplayUnit='m'
        ),
    )
    fivePeriods = SubSection(
        section=Durations,
        description='5-period vs amplitude',
        repeats=True
    )    
    errPeriodA = Quantity(
        type=np.dtype('float64'),
        a_eln=ELNAnnotation(
            component='NumberEditQuantity'
        ),
    )
    errPeriodB = Quantity(
        type=np.dtype('float64'),
        unit='s',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity',
            defaultDisplayUnit='s'
        ),
    )
    errLengthA = Quantity(
        type=np.dtype('float64'),
        a_eln=ELNAnnotation(
            component='NumberEditQuantity'
        ),
    )
    errLengthB = Quantity(
        type=np.dtype('float64'),
        unit='m',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity',
            defaultDisplayUnit='m'
        ),
    )
    errLengthOffset = Quantity(
        type=np.dtype('float64'),
        unit='m',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity',
            defaultDisplayUnit='m'
        ),
    )
    
class _P0_Fadenpendel(_GPR):
    singlePeriods = SubSection(
        section=SinglePeriods,
        description='Period measurements at fixed amplitude and length',
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
        if not self.singlePeriods:
            self.singlePeriods = SinglePeriods(notes='',zeroPoint6=Durations(period=np.zeros(6)),reversePoint6=Durations(period=np.zeros(6)),zeroPoint120=Durations(period=np.zeros(10)),errPeriodA=0,errPeriodB=0)
        if not self.periodVsAmplitude:
            self.periodVsAmplitude = PeriodVsAmplitude(notes='',amplitude=np.zeros(5),errAmplitude=np.zeros(5),fivePeriods=[Durations(period=np.zeros(6))],errPeriodA=0,errPeriodB=0)
        if not self.periodVsLength:
            self.periodVsLength = PeriodVsLength(notes='',length=np.zeros(3),fivePeriods=[Durations(period=np.zeros(6))],errPeriodA=0,errPeriodB=0,errLengthA=0,errLengthB=0,lengthOffset=0,errLengthOffset=0)
