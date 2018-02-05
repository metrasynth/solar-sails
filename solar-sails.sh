#!/usr/bin/env bash
LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libasound.so.2 $(dirname $0)/solar-sails $@
