# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.contrib.auth.models import User


@python_2_unicode_compatible
class Especialidad(models.Model):
    descripcion = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return u'%s' % self.descripcion


@python_2_unicode_compatible
class Consultorio(models.Model):
    numero = models.IntegerField(choices=[(k, k) for k in range(1, 11)])
    especialidad = models.ForeignKey(Especialidad)

    class Meta:
        unique_together = ("numero", "especialidad")

    def __str__(self):
        return u'%s' % self.descripcion


@python_2_unicode_compatible
class Personal(models.Model):
    usuario = models.OneToOneField(User, help_text="Se crea automáticamente cuando se registra el personal",
                                   null=True, blank=True, unique=True, on_delete=models.PROTECT, editable=False)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        try:
            return u'%s' % self.usuario.get_full_name()
        except:
            return u'%s' % self.id


@python_2_unicode_compatible
class Profesional(Personal):
    titulo = models.CharField(max_length=1, default="M", choices=(('M', 'Dr'), ('F', 'Dra')), null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Profesionales'

    def __str__(self):
        try:
            return u'%s %s' % (self.get_titulo_display() if self.titulo else '', self.usuario.get_full_name())
        except:
            return u'%s' % self.id


@python_2_unicode_compatible
class Administrativo(Personal):
    especialidad = models.ForeignKey(Especialidad, null=True, blank=True, help_text="Última especialidad")

    class Meta:
        verbose_name_plural = "Administrativos"

    def __str__(self):
        try:
            return u'%s' % self.usuario.get_full_name()
        except:
            return u'%s' % self.id