from django.db import models
from credential_management_system.settings import MEDIA_URL
from cryptography.fernet import Fernet

STORAGE_TYPE_CHOICES = [
    ('Dedicated', 'Dedicated'),
    ('Non-dedicated', 'Non-dedicated'),
]

# Create your models here.
class Server(models.Model):
    cpu = models.CharField(max_length=150)
    ram = models.IntegerField()
    storage = models.IntegerField()
    password = models.CharField(max_length=150)
    # key = models.CharField(max_length=500)
    key = models.CharField(max_length=500, null=True, blank=True)
    private_ip = models.GenericIPAddressField(null=True, blank=True)
    public_ip = models.GenericIPAddressField(null=True, blank=True)
    type = models.CharField(max_length=150, null=True, blank=True)
    platform_hosted = models.CharField(max_length=150, null=True, blank=True)
    owner = models.CharField(max_length=150, null=True, blank=True)
    storage_type = models.CharField(max_length=150, null=True, blank=True, choices=STORAGE_TYPE_CHOICES)
    online = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.cpu

    def save(self, *args, **kwargs):
        key = Fernet.generate_key()
        f = Fernet(key)
        encrypted_password = f.encrypt(self.password.encode()).decode()
        self.password = encrypted_password
        self.key = key.decode()
        return super(Server, self).save(*args, **kwargs)


class Project(models.Model):
    name = models.CharField(max_length=150)
    owner_client = models.CharField(max_length=150, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='projects')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Profile(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     company = models.ForeignKey(Company, on_delete=models.CASCADE)
#     project = models.ManyToManyField(Project, blank=True)
#     friends = models.ManyToManyField('self', blank=True)
    img = models.ImageField(upload_to= MEDIA_URL + '/profile')


