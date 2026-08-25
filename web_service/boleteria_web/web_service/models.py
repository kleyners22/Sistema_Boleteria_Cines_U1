# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from mongoengine import (Document, StringField, IntField, 
    DateField, ReferenceField
)



class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Cartelera(Document):
    id_cartelera = IntField()
    fecha_inicio = DateField()
    fecha_fin = DateField()
    nombre = StringField(max_length=100)
    meta = {'collection': 'cartelera', 'indexes': ['id_cartelera']}

    def __str__(self):
        return self.nombre or f'Cartelera {self.id_cartelera}'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Pelicula(Document):
    CLASIFICACION_CHOICES = [
        ('AA', 'AA - Todo público niños'),
        ('A', 'A - Todo público familia'),
        ('B', 'B - Adolescentes'),
        ('B15', 'B15 - Mayores de 15'),
        ('C', 'C - Mayores de 18'),
        ('D', 'D - Adultos'),
    ]

    GENERO_CHOICES = [
        ('ACCION', 'ACCION'),
        ('COMEDIA', 'COMEDIA'),
        ('DRAMA', 'DRAMA'),
        ('TERROR', 'TERROR'),
        ('CIENCIA_FICCION', 'CIENCIA_FICCION'),
        ('FANTASIA', 'FANTASIA'),
        ('ROMANCE', 'ROMANCE'),
        ('SUSPENSO', 'SUSPENSO'),
        ('ANIMACION', 'ANIMACION'),
        ('AVENTURA', 'AVENTURA'),
        ('DOCUMENTAL', 'DOCUMENTAL'),
        ('MUSICAL', 'MUSICAL'),
    ]
    id_pelicula = IntField()
    id_cartelera = IntField()
    titulo = StringField(max_length=50)
    duracion = IntField()
    clasificacion = StringField(max_length=4, choices=CLASIFICACION_CHOICES)
    genero = StringField(max_length=20, choices=GENERO_CHOICES)
    meta = {
    'collection': 'pelicula',
    'indexes': ['id_pelicula']
    }

    def __str__(self):
        return self.titulo


class ProyectarPelicula(Document):
    id_proyectar_pelicula = IntField()
    id_pelicula = IntField()
    numero_sala = IntField()
    fecha = DateField()
    hora = StringField(max_length=8)
    meta = {'collection': 'proyectar_pelicula', 'indexes': ['id_proyectar_pelicula']}

    def __str__(self):
        return f'Pelicula {self.id_pelicula} - Sala {self.numero_sala} - {self.fecha} {self.hora}'

class Sala(Document):
    ESTADO_CHOICES = [
    ('ACTIVA', 'ACTIVA'),
    ('INACTIVA', 'INACTIVA'),
    ]
    numero_sala = IntField()
    asientos = IntField()
    estado = StringField(max_length=9, choices=ESTADO_CHOICES)
    meta = {'collection': 'sala', 'indexes': ['numero_sala']}

    def __str__(self):
        return f'Sala {self.numero_sala} ({self.asientos} asientos)'
