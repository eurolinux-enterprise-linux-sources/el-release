#!/bin/bash
########################################################################
# Right now SL doesn't ship with a EULA, but putting this code
#  directly in the trigger seems to create a dep-loop with rpm
#  so we do it here....
########################################################################
SELFCOPIES=${1:-0}
TRIGGERCOPIES=${2:-0}
########################################################################
if [[ -f /usr/lib/python2.7/site-packages/initial_setup/gui/spokes/eula.py ]]; then
    rm -f /usr/lib/python2.7/site-packages/initial_setup/gui/spokes/eula.py*
fi
if [[ -f /usr/lib/python2.7/site-packages/initial_setup/gui/spokes/eula.glade ]]; then
    rm -f /usr/lib/python2.7/site-packages/initial_setup/gui/spokes/eula.glade
fi

if [[ -f /usr/lib/python2.7/site-packages/initial_setup/tui/spokes/eula.py ]]; then
    rm -f /usr/lib/python2.7/site-packages/initial_setup/tui/spokes/eula.py*
fi
