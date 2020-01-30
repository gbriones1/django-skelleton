#!/bin/bash

mysqldump --no-create-info -u root --skip-password modb database_appliance database_brand database_percentage database_provider database_product django_migrations > "seed.sql"
