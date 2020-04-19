from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from datetime import datetime
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from account.validators import validate_phone
from citiesapp.models import City, State


def current_year():
    return datetime.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


def code_generator():
    last_property = Property.objects.all().order_by('id').last()
    # check if it is the first register
    if not last_property:
        code_str = datetime.now().strftime("%y") + datetime.now().strftime("%m") + '0000'
        code = int(code_str)
        return code
    # get letest property's code
    property_code = str(last_property.code)
    code_date = property_code[:4]
    code_unique = (int(property_code[-4:]))
    today_date = datetime.now().strftime("%y%m")
    # creates new code
    if code_date != today_date:
        code_str = today_date + '0000'
        code = int(code_str)
    else:
        code_unique_new = str(code_unique + 1).zfill(4)
        code_str = today_date + code_unique_new
        code = int(code_str)
    return code


class Project(models.Model):
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects', verbose_name=_('manager'))
    name = models.CharField(_('name'), max_length=30)
    name_slug = models.CharField(max_length=50)
    date_start = models.DateField(_('Beginning date'))
    date_complete = models.DateField(_('completion date'))
    photo = models.ImageField(upload_to="media/project", default="/profiles/project.jpg")
    facilities = models.ManyToManyField('Facility', related_name='projects', verbose_name=_('Facilities'))
    description = models.TextField(max_length=255, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name_slug:
            self.name_slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)


class Facility(models.Model):
    name = models.CharField(max_length=40)
    name_slug = models.CharField(max_length=60)

    def save(self, *args, **kwargs):
        if not self.name_slug:
            self.name_slug = slugify(self.name)
        super(Facility, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Property(models.Model):
    APARTMENT = 'APT'
    HOUSE = 'HOU'
    LAND = 'LAN'
    COMMERCIAL = 'COM'
    FARM = 'FAR'

    NEW = 'NEW'
    OFFPLAN = 'PLA'
    STARTED = 'STA'
    USED = 'USE'

    TIPO_PRO = [
        (APARTMENT, _('apartment')),
        (HOUSE, _('house')),
        (LAND, _('land')),
        (FARM, _('farm')),
        (COMMERCIAL, _('commercial')),
    ]
    STATUS_PRO = [
        (NEW, _('new')),
        (OFFPLAN, _('off-plans')),
        (STARTED, _('on construction')),
        (USED, _('used')),
    ]

    code = models.IntegerField(_('code'), default=00000000)
    upload_code = models.IntegerField(_('upload-code'), default=00000000, null=True, blank=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties', verbose_name=_('manager'))
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_properties', verbose_name=_('owner'))
    type_property = models.CharField(_('type of property'), max_length=70, choices=TIPO_PRO, default=APARTMENT)
    condition = models.CharField(_('condition'), max_length=40, choices=STATUS_PRO, default=NEW)
    price = models.DecimalField(_('price'), decimal_places=0, max_digits=12)
    price_str = models.CharField(max_length=18, default="")
    rooms = models.IntegerField(_('rooms'), default=0)
    baths = models.IntegerField(_('bathrooms'), default=0)
    parking = models.IntegerField(_('parking'), default=0)
    area_built = models.DecimalField(_('built area'), default=0, decimal_places=0, max_digits=12)
    area_total = models.DecimalField(_('total area'), default=0, decimal_places=0, max_digits=12)
    estrato = models.IntegerField(null=True, blank=True)
    year = models.PositiveIntegerField(_('built in'), default=current_year(),
                                       validators=[MinValueValidator(1900), max_value_current_year])
    title = models.CharField(_('title'), max_length=30)
    title_slug = models.SlugField(max_length=50)
    description = models.TextField(_('description'), max_length=700)
    type_business = models.ManyToManyField('BusinessType', related_name='business', verbose_name=_('offer type'))

    # analytic
    seen = models.IntegerField(_('seen'), default=0)
    active = models.BooleanField(_('active'), default=False)
    pause = models.BooleanField(_('pause'), default=False)
    promoted = models.BooleanField(_('promoted'), default=False)
    followers = models.ManyToManyField(User, through='Following', related_name='following', )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # project
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, related_name='proj_properties',
                                verbose_name=_('project'), null=True, blank=True)

    class Meta:
        ordering = ('-created',)
        verbose_name_plural = "properties"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.title_slug:
            self.title_slug = slugify(self.title)
        if not self.code:
            self.code = code_generator()
        super(Property, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('property:detail', args=[self.id])


class AddressCol(models.Model):
    propiedad = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='address_col')
    departamento = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    ciudad = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    barrio = models.CharField(max_length=30, null=True, blank=True)
    tipo_via = models.CharField(max_length=30)
    via = models.CharField(max_length=30)
    prefijo_via = models.CharField(max_length=10, null=True, blank=True)
    numero = models.IntegerField()
    prefijo_numero = models.CharField(max_length=10, null=True, blank=True)
    placa = models.IntegerField()
    mostrar = models.BooleanField(default=False)

    def __str__(self):
        if self.mostrar:
            address = "{} {}{} # {}{} - {}, {}, {}".format(self.tipo_via, self.via,
                                                           self.prefijo_via, self.numero,
                                                           self.prefijo_numero, self.placa,
                                                           self.ciudad, self.departamento)
            return address.replace("None", "")
        else:
            if self.barrio:
                return "{}, {}, {}".format(self.barrio, self.ciudad, self.departamento)
            return "{}, {}".format(self.ciudad, self.departamento)


class Following(models.Model):
    user = models.ForeignKey('auth.User', related_name='rel_from_set', on_delete=models.CASCADE)
    property_followed = models.ForeignKey(Property, related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user, self.property_followed)


class BusinessType(models.Model):
    SALE = 'SALE / VENTA'
    RENT = 'RENT / ARRENDAMIENTO'
    SWAP = 'SWAP / PERMUTA'

    TIPO_BUS = [
        (SALE, _('sale')),
        (RENT, _('rent')),
        (SWAP, _('swap')),
    ]
    name = models.CharField(_('type of business'), max_length=70, choices=TIPO_BUS, default=SALE)

    def __str__(self):
        return self.name


class Image(models.Model):
    propiedad = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='img/', default='img/img_1.jpg', null=True, blank=True)
    main = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.propiedad.gallery.all():
            self.main = True
        super(Image, self).save(*args, **kwargs)


class Contact(models.Model):
    propiedad = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(_('name'), max_length=50)
    email = models.EmailField(_('email'), max_length=100, null=True, blank=True)
    phone = models.BigIntegerField(_('phone'), validators=[validate_phone])
    message = models.TextField(_('message'), max_length=500, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
