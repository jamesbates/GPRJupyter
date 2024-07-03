from pydantic import Field
from nomad.config.models.plugins import SchemaPackageEntryPoint
from nomad.metainfo import SchemaPackage
from nomad.datamodel.data import Schema
from nomad.datamodel.metainfo.annotations import ELNAnnotation
from nomad.metainfo import SchemaPackage, Quantity, MSection, Datetime, SubSection
from .P0 import _P0_Fadenpendel

m_package = SchemaPackage()

class P0_Fadenpendel(Schema,_P0_Fadenpendel):
  def normalize(self, archive, logger):
    super().normalize(archive, logger)
    super()._normalize(archive, logger)

m_package.__init_metainfo__()

class GprSchemaEP(SchemaPackageEntryPoint):

  def load(self):
    global m_package
    return m_package

schema_ep = GprSchemaEP()



