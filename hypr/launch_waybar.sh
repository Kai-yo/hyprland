#!/bin/bash

killall -q waybar
sleep 0.5
exec waybar
