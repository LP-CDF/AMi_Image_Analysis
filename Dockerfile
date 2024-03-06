FROM python:3.7-slim-buster

RUN useradd --create-home --shell /bin/bash AMi
WORKDIR /home/AMi

ENV QT_QUICK_BACKEND=software

RUN apt-get update && apt-get install -y --no-install-recommends \
libglib2.0-0 \
python3-pyqt5.qtopengl libxcb-xinerama0 \
evince nano

COPY . ./AMi_Image_Analysis
RUN chown -R AMi ./AMi_Image_Analysis
RUN chgrp -R AMi ./AMi_Image_Analysis

USER AMi
WORKDIR /home/AMi/AMi_Image_Analysis
RUN python3 Setup.py

RUN /home/AMi/python/venvs/AMI_IMAGE_ANALYSIS_TENSORFLOW1/bin/python \
-m pip cache purge

WORKDIR /home/AMi
ENV PATH="/home/AMi/AMi_Image_Analysis/bin:$PATH"
RUN echo 'alias manual="evince /home/AMi/AMi_Image_Analysis/Manual_AMi_Image_Analysis.pdf &"' >> ~/.bashrc
RUN echo 'echo 'TO DISPLAY the manual type "manual"'' >> ~/.bashrc

CMD ["bash"]
