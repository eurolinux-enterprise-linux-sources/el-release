#!/bin/bash

for filename in $(ls `dirname $0`/anaconda-make-service-*.sh); do
    $(${filename})
done

