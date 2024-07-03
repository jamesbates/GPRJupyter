import __main__

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from nomad.client.archive import ArchiveQuery
import nomad.config

from IPython.display import Latex


nomad.config.client.url = 'http://172.17.0.1/nomad-oasis/api'

experimentArchive = ArchiveQuery(
    query={'entry_id': __main__.entry_id},
    required='*',
    username=nomad.config.client.user,
    password=nomad.config.client.password
).download(1)[0]
    
def getData(_expName):
    return pd.DataFrame(experimentArchive.data[_expName].m_to_dict())



pd.options.styler.format.decimal = '.'
pd.options.styler.format.thousands = ' '
pd.options.styler.format.precision = 2
pd.options.styler.latex.hrules = True

class display_wrapper(object):
    def __init__(self, ob, repr_html, repr_latex):
        self.ob = ob
        self.repr_html = repr_html
        self.repr_latex = repr_latex

    def _repr_html_(self):
        return self.repr_html(self.ob)

    def _repr_latex_(self):
        return self.repr_latex(self.ob)


def figure(axes=None):
    _ax = (plt.gca() if axes is None else axes)
    _title = _ax.get_title()
    _ax.set_title(None)
    plt.show()
    display(display_wrapper(
        _title,
        lambda ti: f'<em>Abbildung: {ti}</em>',
        lambda ti: f'\\captionof{{figure}}{{{ti}}}\\vspace{{12pt}}'
    ))

def table(table):
    _table = table.style if isinstance(table, pd.DataFrame) else table
    display(display_wrapper(
        _table.hide(axis=0),
        lambda ta: ta.to_html(caption=f'<em>Tabelle: {ta.caption}</em>'),
        lambda ta: ta.to_latex(position_float='centering',position='H')
    ))

# Use named API:
#import nomad.client.api as api
#auth=api.Auth()
#res = api.get(f'entries/{entryId}/archive',auth=auth)
#experimentData = res.json()['data']['archive']['data']



# Parse archive json:
#from nomad.client import parse
#from IPython.display import Latex

#experimentData = parse('Experiment.archive.json')[0].data
