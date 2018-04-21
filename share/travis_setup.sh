#!/bin/bash
set -evx

mkdir ~/.sanitycore

# safety check
if [ ! -f ~/.sanitycore/.sanity.conf ]; then
  cp share/sanity.conf.example ~/.sanitycore/sanity.conf
fi
