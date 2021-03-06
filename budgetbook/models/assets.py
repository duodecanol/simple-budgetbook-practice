from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from model_utils.managers import InheritanceManager, InheritanceManagerMixin, InheritanceQuerySetMixin

from .currency import Currency
from .helpers import SoftDeleteModel, SoftDeleteManager

User = get_user_model()


class CustomInheritanceManager(SoftDeleteManager, InheritanceManager):
    """ Inheritance 및 SoftDelete Manager를 결합한다.
    단, SoftDeleteManager를 먼저 기재해줘야 is_delete 필드에 대한 필터가 우선 적용된다.
    """
    pass


class Asset(SoftDeleteModel):

    name = models.CharField(_(_('name')), max_length=255)
    amount = models.DecimalField(_('amount'), decimal_places=4, max_digits=65)
    create_date = models.DateTimeField(_('creation date'), auto_now_add=True, editable=False)
    is_active = models.BooleanField(_('is active'), default=True)
    data = models.JSONField(_('related data'), null=True, blank=True)
    owner = models.ForeignKey(User, related_name="assets", null=False, blank=False, on_delete=models.CASCADE)

    objects = CustomInheritanceManager()

    class Meta:  # 추상 클래스이면 super/sub타입이 생기지 않는다
        pass
    #     abstract = True

    def __str__(self):
        return f"[{self.owner}] {self.name}"


class BankAccount(Asset):

    bank_name = models.CharField(_('bank name'), max_length=255)
    account_number = models.CharField(_('bank account number'), max_length=255, unique=True)
    currency = models.ForeignKey(Currency, related_name='bankaccounts', on_delete=models.CASCADE)


class Cash(Asset):
    currency = models.ForeignKey(Currency, related_name=_('cashes'), on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'cash'
        verbose_name_plural = 'cashes'


class CreditCard(Asset):

    card_company_name = models.CharField(_('card company name'), max_length=255)
    #TODO: card number attr+ 암호화해서 저장해야할듯 하여 현재 추가하지 않음.
    currency = models.ForeignKey(Currency, related_name='creditcards', on_delete=models.CASCADE)
    credit_limit = models.DecimalField(
        _('credit limit'),
       decimal_places=4, max_digits=65,
       null=True, blank=True,
       help_text=_('The amount of credit you can use to make your purchases')
    )
    statement_balance = models.DecimalField(
        _('statement balance'),
        decimal_places=4, max_digits=65,
        null=True, blank=True,
        help_text=_(
        'The amount you owe on your credit card as of the latest billing cycle.'
        ' It includes any finance charges and late fees.')
    )
    outstanding_balance = models.DecimalField(
        _('outstanding balance'),
        decimal_places=4, max_digits=65,
        null=True, blank=True,
        help_text=_('Total unpaid amount')
    )
    billing_cycle_date = models.IntegerField(
        _('date of monthly billing cycle'), default=10,
         help_text='월마다 돌아오는 대금납부 지정일'
    )

    

