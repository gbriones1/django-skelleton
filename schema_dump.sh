#!/bin/bash

mysqldump --no-data -u root --skip-password modb > "schema.sql"
