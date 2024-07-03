import __main__

show_out = True
import ipywidgets as w
import qgridnext as qg
from traitlets import All
out = w.Output(layout={'border': '2px solid red'})
if show_out:
    display(out)
with out:
    print(f"Loading entry {__main__.entry_id}")
    
def enable_httplogging():
  import logging
  import contextlib
  from http.client import HTTPConnection

  HTTPConnection.debuglevel = 1

  logging.basicConfig()
  logging.getLogger().setLevel(logging.DEBUG)
  requests_log = logging.getLogger("requests.packages.urllib3")
  requests_log.setLevel(logging.DEBUG)
  requests_log.propagate = True

#enable_httplogging()

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


with out:
  from nomad.client.archive import ArchiveQuery
  import nomad.client.api
  import nomad.config

  nomad.config.client.url = 'http://172.17.0.1/nomad-oasis/api'

  auth = nomad.client.api.Auth()

from IPython.display import Latex, Markdown

def buildDataFrame(data):
    df=pd.DataFrame(data)
    df.index.name='Messung'
    df.index+=1
    return df

def readExperiment():
  global experimentArchive
  experimentArchive = ArchiveQuery(
        query={'entry_id': __main__.entry_id },
        required=None,
        username=nomad.config.client.user,
        password=nomad.config.client.password
    ).download(1)[0]
  

def writeExperiment():
    global experimentArchive
    response = nomad.client.api.put(f"uploads/{experimentArchive.metadata.upload_id}/raw/",
        auth=auth,
        params={"file_name":experimentArchive.metadata.mainfile, "wait_for_processing": True, "include_archive": False, "entry_hash": experimentArchive.metadata.entry_hash},
        json={'data': experimentArchive.data.m_to_dict()}
    )
    if response.status_code == 200:
        return True
    else:
        with out:
            print(f"Save ERROR: {response.status_code}: {response.content}")
        return False

with out:
    readExperiment()

wSaved = w.Valid(
    description='Saved',
    readout='',
    value=True,
    layout={'width': '500px', 'height': '50px'}
)
wSinglePeriodLength = w.FloatText(
    value=experimentArchive.data.singlePeriod.length.magnitude,
    description='Pendellänge [m]:',
    disabled=False,
    style={'description_width': '100px'}
)
wSinglePeriodAmplitude = w.FloatText(
    value=experimentArchive.data.singlePeriod.amplitude.magnitude,
    description='Auslenkung [$\\degree$]:',
    disabled=False,
    style={'description_width': '100px'}
)
wSinglePeriodZeroPoint = qg.show_grid(
    buildDataFrame({'Periode [s]': experimentArchive.data.singlePeriod.m_to_dict()['zeroPoint']}),
    show_toolbar=True
)
wSinglePeriodReversePoint = qg.show_grid(
    buildDataFrame({'Periode [s]': experimentArchive.data.singlePeriod.m_to_dict()['reversePoint']}),
    show_toolbar=True
)
wSinglePeriodNotes = w.Textarea(
    value=experimentArchive.data.singlePeriod.notes,
    placeholder='(Notizen)',
    description='Notizen:',
    disabled=False,
    layout={'width': '80%', 'height': '100px'},
    continuous_update=False
)


wTenPeriodsLength = w.FloatText(
    value=experimentArchive.data.tenPeriods.length.magnitude,
    description='Pendellänge [m]:',
    disabled=False,
    style={'description_width': '100px'}
)
wTenPeriodsAmplitude = w.FloatText(
    value=experimentArchive.data.tenPeriods.amplitude.magnitude,
    description='Auslenkung [$\\degree$]:',
    disabled=False,
    style={'description_width': '100px'}
)
wTenPeriodsZeroPoint = qg.show_grid(
    buildDataFrame({'10 Perioden [s]': experimentArchive.data.tenPeriods.m_to_dict()['zeroPoint']}),
    show_toolbar=True
)
wTenPeriodsReversePoint = qg.show_grid(
    buildDataFrame({'10 Perioden [s]': experimentArchive.data.tenPeriods.m_to_dict()['reversePoint']}),
    show_toolbar=True
)
wTenPeriodsNotes = w.Textarea(
    value=experimentArchive.data.tenPeriods.notes,
    placeholder='(Notizen)',
    description='Notizen:',
    disabled=False,
    layout={'width': '80%', 'height': '100px'},
    continuous_update=False
)

wPeriodVsAmplitudeLength = w.FloatText(
    value=experimentArchive.data.periodVsAmplitude.length.magnitude,
    description='Pendellänge [m]:',
    disabled=False,
    style={'description_width': '100px'}
)
wPeriodVsAmplitudeData = qg.show_grid(
    buildDataFrame({
        'Amplitude [$\\degree$]': experimentArchive.data.periodVsAmplitude.m_to_dict()['amplitude'],
        '10 Perioden [s]': experimentArchive.data.periodVsAmplitude.m_to_dict()['period']
    }),
    show_toolbar=True
)
wPeriodVsAmplitudeNotes = w.Textarea(
    value=experimentArchive.data.periodVsAmplitude.notes,
    placeholder='(Notizen)',
    description='Notizen:',
    disabled=False,
    layout={'width': '80%', 'height': '100px'},
    continuous_update=False
)

wPeriodVsLengthAmplitude = w.FloatText(
    value=experimentArchive.data.periodVsLength.amplitude.magnitude,
    description='Amplitude [$\\degree$]:',
    disabled=False,
    style={'description_width': '100px'}
)
wPeriodVsLengthData = qg.show_grid(
    buildDataFrame({
        'Pendellänge [m]': experimentArchive.data.periodVsLength.m_to_dict()['length'],
        '10 Perioden [s]': experimentArchive.data.periodVsLength.m_to_dict()['period']
    }),
    show_toolbar=True
)
wPeriodVsLengthNotes = w.Textarea(
    value=experimentArchive.data.periodVsLength.notes,
    placeholder='(Notizen)',
    description='Notizen:',
    disabled=False,
    layout={'width': '80%', 'height': '100px'},
    continuous_update=False
)


#@out.capture(clear_output=True)
def updateData(change):
    global experimentArchive
    
    wSaved.value = False
    print(f"L Received change event, change/event = {change}")
    experimentArchive.data.singlePeriod.amplitude = wSinglePeriodAmplitude.value  
    experimentArchive.data.singlePeriod.length = wSinglePeriodLength.value  
    experimentArchive.data.singlePeriod.zeroPoint = wSinglePeriodZeroPoint.get_changed_df()['Periode [s]']  
    experimentArchive.data.singlePeriod.reversePoint = wSinglePeriodReversePoint.get_changed_df()['Periode [s]']  
    experimentArchive.data.singlePeriod.notes = wSinglePeriodNotes.value  
    experimentArchive.data.tenPeriods.amplitude = wTenPeriodsAmplitude.value  
    experimentArchive.data.tenPeriods.length = wTenPeriodsLength.value  
    experimentArchive.data.tenPeriods.zeroPoint = wTenPeriodsZeroPoint.get_changed_df()['10 Perioden [s]']  
    experimentArchive.data.tenPeriods.reversePoint = wTenPeriodsReversePoint.get_changed_df()['10 Perioden [s]']  
    experimentArchive.data.tenPeriods.notes = wTenPeriodsNotes.value  
    experimentArchive.data.periodVsAmplitude.length = wPeriodVsAmplitudeLength.value  
    experimentArchive.data.periodVsAmplitude.period = wPeriodVsAmplitudeData.get_changed_df()['10 Perioden [s]']  
    experimentArchive.data.periodVsAmplitude.amplitude = wPeriodVsAmplitudeData.get_changed_df()['Amplitude [$\\degree$]']  
    experimentArchive.data.periodVsAmplitude.notes = wPeriodVsAmplitudeNotes.value  
    experimentArchive.data.periodVsLength.amplitude = wPeriodVsLengthAmplitude.value  
    experimentArchive.data.periodVsLength.period = wPeriodVsLengthData.get_changed_df()['10 Perioden [s]']  
    experimentArchive.data.periodVsLength.length = wPeriodVsLengthData.get_changed_df()['Pendellänge [m]']  
    experimentArchive.data.periodVsLength.notes = wPeriodVsLengthNotes.value  
    
    if writeExperiment():
        readExperiment()

        wSinglePeriodAmplitude.value = experimentArchive.data.singlePeriod.amplitude.magnitude
        wSinglePeriodLength.value = experimentArchive.data.singlePeriod.length.magnitude
        wSinglePeriodZeroPoint.df = buildDataFrame({'Periode [s]': experimentArchive.data.singlePeriod.zeroPoint})
        wSinglePeriodReversePoint.df = buildDataFrame({'Periode [s]': experimentArchive.data.singlePeriod.reversePoint})
        wSinglePeriodNotes.value = experimentArchive.data.singlePeriod.notes
        wTenPeriodsAmplitude.value = experimentArchive.data.tenPeriods.amplitude.magnitude
        wTenPeriodsLength.value = experimentArchive.data.tenPeriods.length.magnitude
        wTenPeriodsZeroPoint.df = buildDataFrame({'10 Perioden [s]': experimentArchive.data.tenPeriods.zeroPoint})
        wTenPeriodsReversePoint.df = buildDataFrame({'10 Perioden [s]': experimentArchive.data.tenPeriods.reversePoint})
        wTenPeriodsNotes.value = experimentArchive.data.tenPeriods.notes
        wPeriodVsAmplitudeLength.value = experimentArchive.data.periodVsAmplitude.length.magnitude
        wPeriodVsAmplitudeData.df = buildDataFrame({
            'Amplitude [$\\degree$]': experimentArchive.data.periodVsAmplitude.m_to_dict()['amplitude'],
            '10 Perioden [s]': experimentArchive.data.periodVsAmplitude.m_to_dict()['period']
        })
        wPeriodVsAmplitudeNotes.value = experimentArchive.data.periodVsAmplitude.notes  
        wPeriodVsLengthAmplitude.value = experimentArchive.data.periodVsLength.amplitude.magnitude
        wPeriodVsLengthData.df = buildDataFrame({
            'Pendellänge [m]': experimentArchive.data.periodVsLength.m_to_dict()['length'],
            '10 Perioden [s]': experimentArchive.data.periodVsLength.m_to_dict()['period']
        })
        wPeriodVsLengthNotes.value = experimentArchive.data.periodVsLength.notes  
        wSaved.value = True


display(
    Markdown(f'''
# {experimentArchive.data.lab_name}
'''),
    wSaved,
    Markdown(f'''

## Einzelperiodenmessung
'''),
    wSinglePeriodLength,
    wSinglePeriodAmplitude,
    Markdown('Periodenmessung beim Nullpunktdurchgang'),
    wSinglePeriodZeroPoint,
    Markdown('Periodenmessung beim Umkehrpunkt'),
    wSinglePeriodReversePoint,
    wSinglePeriodNotes,
    wSaved,
    Markdown(f'''

## 10-Periodenmessung
'''),
    wTenPeriodsLength,
    wTenPeriodsAmplitude,
    Markdown('10-Periodenmessung beim Nullpunktdurchgang'),
    wTenPeriodsZeroPoint,
    Markdown('10-Periodenmessung beim Umkehrpunkt'),
    wTenPeriodsReversePoint,
    wTenPeriodsNotes,
    wSaved,
    Markdown(f'''

## Amplitudenabhängige Periodenmessung
'''),
    wPeriodVsAmplitudeLength,
    wPeriodVsAmplitudeData,
    wPeriodVsAmplitudeNotes,
    wSaved,
    Markdown(f'''

## Längenabhängige Periodenmessung
'''),
    wPeriodVsLengthAmplitude,
    wPeriodVsLengthData,
    wPeriodVsLengthNotes,
    wSaved

)

wSinglePeriodLength.observe(handler=updateData, names='value') 
wSinglePeriodAmplitude.observe(handler=updateData, names='value')
wSinglePeriodZeroPoint.on('cell_edited', lambda e,w: updateData(e))
wSinglePeriodReversePoint.on('cell_edited', lambda e,w: updateData(e))
wSinglePeriodNotes.observe(handler=updateData, names='value')
wTenPeriodsLength.observe(handler=updateData, names='value') 
wTenPeriodsAmplitude.observe(handler=updateData, names='value')
wTenPeriodsZeroPoint.on('cell_edited', lambda e,w: updateData(e))
wTenPeriodsReversePoint.on('cell_edited', lambda e,w: updateData(e))
wTenPeriodsNotes.observe(handler=updateData, names='value')
wPeriodVsAmplitudeLength.observe(handler=updateData, names='value')
wPeriodVsAmplitudeData.on('cell_edited', lambda e,w: updateData(e))
wPeriodVsAmplitudeNotes.observe(handler=updateData, names='value')
wPeriodVsLengthAmplitude.observe(handler=updateData, names='value')
wPeriodVsLengthData.on('cell_edited', lambda e,w: updateData(e))
wPeriodVsLengthNotes.observe(handler=updateData, names='value')
