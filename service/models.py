import datetime
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import models

User = get_user_model()


class Payment(models.Model):
    amount = models.PositiveBigIntegerField(
        verbose_name='Сумма платежа',
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )
    payment_date = models.DateTimeField(
        verbose_name='Дата платежа',
        auto_now_add=True
    )

    collect = models.ForeignKey(
        verbose_name='Сбор',
        to='Collect',
        on_delete=models.CASCADE,
        related_name='payments'
    )

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return f"{self.amount} ({self.payment_date})"

    def save(self, *args, **kwargs):
        cache.delete('collects')
        return super().save(*args, **kwargs)


class Reason(models.Model):
    name = models.CharField(
        verbose_name='Причина сбора',
        max_length=30
    )

    class Meta:
        verbose_name = 'Причина'
        verbose_name_plural = 'Причины'

    def __str__(self):
        return self.name


class Collect(models.Model):
    author = models.ForeignKey(
        verbose_name='Автор сбора',
        to=User,
        on_delete=models.CASCADE
    )
    title = models.CharField(
        verbose_name='Название',
        max_length=50
    )
    reason = models.ForeignKey(
        verbose_name='Повод',
        to='Reason',
        on_delete=models.CASCADE,
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    goal = models.FloatField(
        verbose_name='Цель',
        default=None,
        null=True
    )
    current_amount = models.IntegerField(
        verbose_name='Собранная сумма',
        default=0
    )
    users_count = models.IntegerField(
        verbose_name='Кол-во участников',
        default=0
    )
    image = models.ImageField(
        verbose_name='Обложка',
        upload_to='%Y/%m/%d',
        null=True,
    )
    deadline = models.DateTimeField(
        verbose_name='Дата завершения сбора',
        default=datetime.datetime.now() + datetime.timedelta(days=30)
    )

    class Meta:
        verbose_name = 'Сбор'
        verbose_name_plural = 'Сборы'

    def __str__(self):
        return f"{self.author} {self.title}"

    def save(self, *args, **kwargs):
        cache.delete('collects')
        return super().save(*args, **kwargs)
