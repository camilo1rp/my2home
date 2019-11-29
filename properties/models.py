from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

# Create your models here.
from django.utils.text import slugify


class Property(models.Model):
    code = models.IntegerField()
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_properties')
    type_property = models.CharField(max_length=70)
    price = models.DecimalField(decimal_places=0, max_digits=12)
    rooms = models.IntegerField(default=0)
    baths = models.IntegerField(default=0)
    parking = models.IntegerField(default=0)
    area_built = models.DecimalField(default=0, decimal_places=0, max_digits=12)
    area_total = models.DecimalField(default=0, decimal_places=0, max_digits=12)
    estrato = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=50)
    title_slug = models.SlugField(max_length=70)
    description = models.TextField(max_length=500)
    type_business = models.CharField(max_length=100)

    # analytic
    seen = models.IntegerField(default=0)
    following = models.IntegerField(default=0)
    followers = models.ManyToManyField(User, through='Following')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.code:
            self.code = self.code_generator()
        super(Property, self).save(*args, **kwargs)

    def code_generator(self):
        last_property = self.objects.all().order_by('id').last()
        # check if it is the first register
        if not last_property:
            code_str = datetime.now().strftime("%y") + datetime.now().strftime("%m") + '0000'
            code = int(code_str)
            return code
        # get letest property's code
        property_code = str(last_property.code)
        code_date = property_code[:4]
        code_unique = int(property_code[-4:])
        today_date = datetime.now().strftime("%y%m")
        # creates new code
        if code_date != today_date:
            code_str = today_date + '0000'
            code = int(code_str)
        else:
            code_unique_new = str(code_unique + 1)
            code_str = today_date + code_unique_new
            code = int(code_str)
        return code


class addressCol(models.Model):
    propiedad = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='address_col')
    Departamento = models.CharField(max_length=30)
    ciudad = models.CharField(max_length=30)
    barrio = models.CharField(max_length=30)
    tipo_via = models.CharField(max_length=30)
    via = models.CharField(max_length=30)
    prefijo_via = models.CharField(max_length=10)
    numero = models.IntegerField()
    prefijo_numero = models.CharField(max_length=10)
    placa = models.IntegerField()
    display = models.BooleanField(default=False)

    def __str__(self):
        return "{} {} {} # {}{} - {}".format(self.tipo_via, self.via, self.prefijo_via,
                                             self.numero, self.prefijo_numero, self.placa)


class Following(models.Model):
    user = models.ForeignKey('auth.User', related_name='rel_from_set', on_delete=models.CASCADE)
    property_followed = models.ForeignKey(Property, related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user, self.property_followed)