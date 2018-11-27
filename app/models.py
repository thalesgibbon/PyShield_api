from django.db import models

class Py_Log_mssql(models.Model):
    _DATABASE = 'mssql'
    class Meta:

        managed = False
        db_table = "[DW].[PY_LOG]"
        #print(db_table)
    pylog_id = models.IntegerField(primary_key=True)
    pylog_etapa_id = models.IntegerField()
    pylog_desc = models.CharField(max_length=200)
    pylog_datetime = models.DateTimeField(auto_now=False)
    def __str__(self):
        return self.pylog_desc
