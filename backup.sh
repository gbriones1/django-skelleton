#!/bin/bash

mkdir -p backup
mysqldump -u root -ppass modb > "backup/latest.sql"
