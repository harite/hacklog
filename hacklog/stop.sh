#!/bin/sh
pid=$(ps aux | grep server.py | grep -v grep | awk '{ print $2}')
kill -HUP $pid
