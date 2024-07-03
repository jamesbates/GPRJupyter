FROM "quay.io/jupyter/scipy-notebook"
USER ${NB_UID}

WORKDIR /tmp
RUN git clone https://gitlab.mpcdf.mpg.de/nomad-lab/nomad-FAIR.git
WORKDIR /tmp/nomad-FAIR
RUN git submodule update --init --recursive

RUN pip --no-cache-dir install .


USER root

RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends \
    texlive-full \
    texlive-fonts-extra && \
    apt-get clean


COPY gpr /tmp/gpr
COPY GPRSchemas /tmp/GPRSchemas
COPY _jupyter ${HOME}/.jupyter
COPY _local/share/jupyter/nbconvert ${HOME}/.local/share/jupyter/nbconvert

RUN chown -R ${NB_UID}:${NB_GID} /tmp/gpr && \
    chown -R ${NB_UID}:${NB_GID} /tmp/GPRSchemas && \
    chown -R ${NB_UID}:${NB_GID} ${HOME}/.local/share/jupyter && \
    chown -R ${NB_UID}:${NB_GID} ${HOME}/.jupyter


USER ${NB_UID}
RUN pip --no-cache-dir install qgridnext voila
WORKDIR /tmp/gpr
RUN pip --no-cache-dir install .
WORKDIR /tmp/GPRSchemas
RUN pip --no-cache-dir install .
WORKDIR ${HOME}
RUN rm -r /tmp/gpr /tmp/GPRSchemas /tmp/nomad-FAIR


