from __future__ import unicode_literals

from django.apps import AppConfig

import os
import shutil
import datetime

class WarehouseConfig(AppConfig):
    name = 'warehouse'


class BackupManager(object):

    # DIRECTORY = os.path.join(os.getcwd(), "backups")# if settings.DEBUG else "C:\\MODB\\backups/"
    DIRECTORY = "C:\\MODB\\backups/"

    def get_current_db(self):
        #if settings.DEBUG:
        # return os.path.join(os.getcwd(), "db.sqlite3")
        #else:
        return "C:\\MODB\\db.sqlite3"

    def get_backups(self):
        backups = []
        for db in os.listdir(BackupManager.DIRECTORY):
            if len(db) == 24 and db.endswith(".sqlite3") and db.startswith("db") and db[2:-8].isdigit():
                formatted_date = db[2:-8][:4]+"-"+db[2:-8][4:6]+"-"+db[2:-8][6:8]+" "+db[2:-8][8:10]+":"+db[2:-8][10:12]+":"+db[2:-8][12:14]
                backups.append((db, formatted_date))
        return backups

    def create_backup(self):
        current_db = self.get_current_db()
        new_db = os.path.join(BackupManager.DIRECTORY, "db"+datetime.datetime.now().strftime('%Y%m%d%H%M%S')+".sqlite3")
        shutil.copy(current_db, new_db)

    def restore_backup(self, backup_file):
        current_db = self.get_current_db()
        new_db = os.path.join(BackupManager.DIRECTORY, backup_file)
        shutil.copy(new_db, current_db)

    def delete_backup(self, backup_file):
        os.remove(os.path.join(BackupManager.DIRECTORY, backup_file))

    def upload_backup(self, file):
        pass
