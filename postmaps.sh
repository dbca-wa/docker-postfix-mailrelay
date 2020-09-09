#!/bin/bash
mkdir /etc/postmaps
cp -v /etc/postmapconfig/*_maps /etc/postmaps
postmap /etc/postmaps/*
