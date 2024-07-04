from pydantic import Field
from nomad.config.models.plugins import SchemaPackageEntryPoint
from nomad.metainfo import SchemaPackage
from nomad.datamodel.data import Schema
from nomad.datamodel.metainfo.annotations import ELNAnnotation
from nomad.metainfo import SchemaPackage, Quantity, MSection, Datetime, SubSection

class Experiment(MSection):
  notes = Quantity(
    type=str,
    description='Notizen',
    a_eln=ELNAnnotation(component='RichTextEditQuantity')
  )

class Participant(MSection):
  participant_name = Quantity(
    type=str,
    description='Name',
    a_eln=ELNAnnotation(component='StringEditQuantity')
  )
  participant_matrikel = Quantity(
    type=str,
    description='Matrikelnr',
    a_eln=ELNAnnotation(component='StringEditQuantity')
  )

class _GPR(MSection):
  lab_name = Quantity(
    type=str,
    description='Versuchsname',
    a_eln=ELNAnnotation(component='StringEditQuantity')
  )
  lab_date = Quantity(
    type=Datetime,
    description='Versuchsdatum',
    a_eln=ELNAnnotation(component='DateTimeEditQuantity')
  )
  lab_participant = SubSection(
    section=Participant,
    repeats=True,
    description='Teilnehmer'
  )




