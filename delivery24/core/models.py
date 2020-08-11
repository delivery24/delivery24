import uuid
import secrets
import string

from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


VERIFF_CODE_LEN = 4
ORDER_ID_LEN = 8


def gen_unique_order_id():
    return ''.join(secrets.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits)
                   for _ in range(ORDER_ID_LEN))


class Work(models.Model):
    WORK_STATUS = [
        (1, 'Not started'),
        (2, 'In progress'),
        (3, 'Done'),
        (4, 'Canceled'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    driver = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.SET_NULL,
                               blank=True,
                               null=True,)
    deliver_from = models.CharField(max_length=500)
    deliver_to = models.CharField(max_length=500)
    delivery_start = models.DateTimeField()
    delivery_end = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()
    status = models.IntegerField(choices=WORK_STATUS)
    order_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f'Deliver from: {self.deliver_from}\nDeliver to: {self.deliver_to}\n' \
               f'Date start: {self.delivery_start}\nDate end: {self.delivery_end}\nDriver: {self.driver}'


class Order(models.Model):
    PAYMENT_METHOD = [
        (1, _('Cash')),
        #(2, _('Bank')),
    ]
    order_id = models.SlugField(unique=True, max_length=ORDER_ID_LEN)
    first_name = models.CharField(_('first name'), max_length=100)
    last_name = models.CharField(_('last name'), max_length=100)
    email = models.EmailField(_('email'), max_length=254)
    phone = PhoneNumberField(_('phone'), help_text=_('Contact phone number'))
    address_from = models.CharField(_('address from'), max_length=128)
    address_to = models.CharField(_('address to'), max_length=128)
    delivery_start = models.DateTimeField(_('delivery start'))
    delivery_end = models.DateTimeField(_('delivery end'))
    movers_num = models.IntegerField(_('number of required movers'),
                                     choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4')],
                                     default=0)
    message = models.TextField(_('message'), help_text=_('additional information'), blank=True)
    payment = models.IntegerField(_('payment method'), choices=PAYMENT_METHOD, default=PAYMENT_METHOD[0][0])
    verified = models.BooleanField(default=False)
    verification_code = models.CharField(unique=True, null=True, max_length=VERIFF_CODE_LEN,
                                         validators=[MinLengthValidator(VERIFF_CODE_LEN)])
    verification_code_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    work = models.ForeignKey(Work,
                             on_delete=models.SET_NULL,
                             blank=True,
                             null=True,
                             related_name='works',
                             related_query_name='work')
    drivers_notified = models.BooleanField(default=False)
    no_free_drivers = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.order_id:  # new object creating
            unique_id = gen_unique_order_id()
            is_exists = Order.objects.filter(order_id=unique_id).exists()
            while is_exists:
                unique_id = gen_unique_order_id()
                is_exists = Order.objects.filter(order_id=unique_id).exists()
            self.order_id = unique_id
        super(Order, self).save()

    def __str__(self):
        return self.email
