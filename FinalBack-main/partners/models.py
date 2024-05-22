from datetime import datetime
from django.db import models
from users.models import User
class ResCountry(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=2, null=True, blank=True, unique=True)
    name = models.CharField(max_length=255, unique=True)

#City state_id
class ResCountryState(models.Model):
    code = models.CharField(max_length=3)
    create_date = models.DateTimeField(null=True)
    name = models.CharField(max_length=255)
    country = models.ForeignKey(ResCountry, on_delete=models.SET_NULL, null=True)
    write_date = models.DateTimeField(null=True)
    region = models.CharField(max_length=255, null=True)

class ResLocalite(models.Model):
    id = models.AutoField(primary_key=True)
    create_uid = models.IntegerField(null=True)
    create_date = models.DateTimeField(null=True)
    name = models.CharField(max_length=30, null=True)
    write_uid = models.IntegerField(null=True)
    write_date = models.DateTimeField(null=True)
    localite_code = models.IntegerField(null=True)
    code_ville = models.IntegerField(null=True)

class Company(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)

class Partners(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    create_date = models.DateTimeField(blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    display_name = models.CharField(max_length=255, blank=True, null=True)

    mobile = models.CharField(max_length=255, blank=True, null=True)
    image_small = models.BinaryField(blank=True, null=True)
    image = models.BinaryField(blank=True, null=True)
    image_medium = models.BinaryField(blank=True, null=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)

    street = models.CharField(max_length=255, blank=True, null=True) #Adresse
    street2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    country_id = models.ForeignKey(ResCountry,  on_delete=models.CASCADE, null=True)
    state_id = models.ForeignKey(ResCountryState,  on_delete=models.CASCADE, null=True)
    localite_id = models.ForeignKey(ResLocalite,  on_delete=models.CASCADE, null=True)
    zip = models.CharField(max_length=24, blank=True, null=True)

    company_id = models.IntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    ean13 = models.CharField(max_length=13, blank=True, null=True)
    color = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    title = models.IntegerField(blank=True, null=True)
    function = models.CharField(max_length=255, blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)
    supplier = models.BooleanField(null=True)
    ref = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    is_company = models.BooleanField(null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    customer = models.BooleanField(null=True)
    fax = models.CharField(max_length=255, blank=True, null=True)
    employee = models.BooleanField(null=True)
    credit_limit = models.FloatField(blank=True, null=True)
    write_date = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(null=True)
    tz = models.CharField(max_length=64, blank=True, null=True)
    write_uid = models.IntegerField(blank=True, null=True)
    lang = models.CharField(max_length=255, blank=True, null=True)
    create_uid = models.IntegerField(blank=True, null=True)

    type = models.CharField(max_length=255, blank=True, null=True)
    use_parent_address = models.BooleanField(null=True)

    birthdate = models.CharField(max_length=255, blank=True, null=True)
    vat = models.CharField(max_length=255, blank=True, null=True)

    commercial_partner_id = models.IntegerField(blank=True, null=True)
    notify_email = models.CharField(max_length=255, null=False)
    message_last_post = models.DateTimeField(blank=True, null=True)
    opt_out = models.BooleanField(null=True)
    signup_type = models.CharField(max_length=255, blank=True, null=True)
    signup_expiration = models.DateTimeField(blank=True, null=True)
    signup_token = models.CharField(max_length=255, blank=True, null=True)
    last_reconciliation_date = models.DateTimeField(blank=True, null=True)
    vat_subjected = models.BooleanField(null=True)
    debit_limit = models.FloatField(blank=True, null=True)
    calendar_last_notif_ack = models.DateTimeField(blank=True, null=True)
    categ_id = models.IntegerField(blank=True, null=True)
    speaker = models.BooleanField(null=True)
    x_art = models.CharField(max_length=32, blank=True, null=True)
    x_date_rc = models.DateField(blank=True, null=True)
    x_nis = models.CharField(max_length=32, blank=True, null=True)
    x_nif = models.CharField(max_length=32, blank=True, null=True)
    x_rc = models.CharField(max_length=32, blank=True, null=True)
    x_tin = models.CharField(max_length=64, blank=True, null=True)
    section_id = models.IntegerField(blank=True, null=True)
    old_code = models.CharField(max_length=255, blank=True, null=True)
    activity_id = models.IntegerField(blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    state = models.CharField(max_length=255,null=False)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    sector_id = models.IntegerField(blank=True, null=True)
    branche_id = models.IntegerField(blank=True, null=True)
    old_account_code = models.CharField(max_length=255, blank=True, null=True)
    parent_partner_id = models.IntegerField(blank=True, null=True)
    is_project = models.BooleanField(null=True)
    debit_limit_other = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    multi_rc = models.BooleanField(null=True)
    is_registre = models.BooleanField(null=True)
    blacklisted = models.BooleanField(null=True)
    credit_limit_other = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_person = models.BooleanField(null=True)
    is_actionnaire = models.CharField(max_length=255, blank=True, null=True)
    fiscality_in_group = models.CharField(max_length=255, blank=True, null=True)
    is_group = models.BooleanField(null=True)
    x_is_professional_non_commercial = models.BooleanField(null=True)
    x_is_bnc = models.BooleanField(null=True)
    x_identity_ref_issuing_authority = models.CharField(max_length=255, blank=True, null=True)


'''new_partner = Partners.objects.create(
    id=90000,
    name='user',
    notify_email= 'email',
    state= 'state'
)
new_partner.save()'''