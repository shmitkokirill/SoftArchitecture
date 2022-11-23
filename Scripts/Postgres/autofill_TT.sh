#!/bin/bash

export PGPASSWORD='111'; psql -h '172.17.0.2' -U 'kirill' -d 'university' -c 'select * from Lesson;'
