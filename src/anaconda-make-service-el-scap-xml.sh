#!/bin/bash
########################################################################
# Anaconda uses a custom yum root, so we need to link our custom
# vars into there
########################################################################
SELFCOPIES=${1:-0}
TRIGGERCOPIES=${2:-0}
########################################################################
echo '[Unit]' > /usr/lib/systemd/system/anaconda-el-scap.service
echo 'ConditionPathExists=/etc/anaconda.repos.d' >> /usr/lib/systemd/system/anaconda-el-scap.service
echo 'Description=Setup SL Anaconda repos' >> /usr/lib/systemd/system/anaconda-el-scap.service
echo '[Install]' >> /usr/lib/systemd/system/anaconda-el-scap.service
echo 'WantedBy=anaconda.target' >> /usr/lib/systemd/system/anaconda-el-scap.service
echo '[Service]' >> /usr/lib/systemd/system/anaconda-el-scap.service
echo 'ExecStart=/usr/libexec/sl-release/anaconda-el-scap-xml.sh' >> /usr/lib/systemd/system/anaconda-el-scap.service

########################################################################
systemctl enable anaconda-el-scap.service
########################################################################

