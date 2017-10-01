#!/bin/bash

mkdir backup
mysqldump -u root -ppass django_test_2 > "backup/latest.sql"
