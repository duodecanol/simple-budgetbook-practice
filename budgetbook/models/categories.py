from django.db import models
from django.contrib.auth import get_user_model

from .helpers import SoftDeleteModel

User = get_user_model()


class TransactionClassification(models.IntegerChoices):
    EXPENSE = 0
    INCOME = 1
    TRANSFER = 2


class Category(SoftDeleteModel):
    """
    expense / income 항목에 대한 카테고리
    초기 버전에서는 고정된 카테고리 항목을 제공하고
    추후에 유저에 따라 Customize된 카테고리 항목을 가질 수 있도록 한다.
    """
    name = models.CharField('category name', max_length=128, null=False, blank=False)
    parent = models.ForeignKey('self', related_name='subcategories',
                               null=True, blank=True,
                               on_delete=models.CASCADE)
    description = models.CharField('category description', max_length=255, null=True, blank=True)
    classification = models.IntegerField('classification for transaction',
                                         choices=TransactionClassification.choices,
                                         default=TransactionClassification.EXPENSE)
    create_date = models.DateTimeField('created datetime', auto_now_add=True, editable=False)
    last_modified = models.DateTimeField('last modified datetime', auto_now=True)
    is_active = models.BooleanField('is Active', default=True,
                                    help_text='사용자가 활성화/비활성화를 지정하여 복구할수도 있음')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f"[{self.parent}] {self.name}" if self.parent else self.name

    @property
    def subcategories(self):
        return self.children.filter(is_active=True)


    def enable(self):
        """ Enable category status"""
        self.is_active = True

    def disable(self):
        """ Disable category status"""
        self.is_active = False

    def toggle(self):
        """ Toggle category status"""
        if self.is_active:
            self.disable()
        else:
            self.enable()

