#!/bin/bash
########################################################################
# scap anaconda addon looks in a specific place for the scap guide
# make sure the file is there
########################################################################

if [[ -f /etc/os-release ]]; then
    . /etc/os-release
    MAJORVERSION=$(echo ${VERSION_ID} | cut -d '.' -f1)
else
    MAJORVERSION='7'
fi

if [[ -f /usr/share/xml/scap/ssg/content/ssg-sl${MAJORVERSION}-xccdf.xml ]]; then
  if [[ ! -f /usr/share/xml/scap/ssg/content/ssg-scientific${MAJORVERSION}-xccdf.xml ]]; then
      ln -s /usr/share/xml/scap/ssg/content/ssg-sl${MAJORVERSION}-xccdf.xml /usr/share/xml/scap/ssg/content/ssg-scientific${MAJORVERSION}-xccdf.xml
  fi
fi

