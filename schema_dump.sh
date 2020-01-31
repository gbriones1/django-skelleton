#!/bin/bash

mysqldump --no-data -u root -ppass modb > "schema.sql"
