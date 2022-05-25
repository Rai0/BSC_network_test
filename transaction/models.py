from django.db import models as m

# Create your models here.

class transactionModel (m.Model):
    date = m.DateTimeField (verbose_name="Дата", auto_now_add=True)
    transactionID = m.CharField (verbose_name="id транзакции", max_length=255,blank=False, db_index=True)
    description = m.TextField (verbose_name="описание транзакции", blank=True)
    
    class Meta:
        verbose_name ="Транзакция"
        verbose_name_plural ="Транзакции"
        ordering = ['-date']
    
    def __str__(self) -> str:
        return self.transactionID