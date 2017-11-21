# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from consultorios.models import Profesional, Administrativo


@admin.register(Profesional)
class ProfesionalAdmin(admin.ModelAdmin):
    readonly_fields = ('usuario',)

    def save_model(self, request, obj, form, change):
        from django.contrib.auth.models import User
        if 'nombre' in form.changed_data or 'apellido' in form.changed_data or 'email' in form.changed_data:
            if 'nombre' in form.initial:
                nombre = form.cleaned_data['nombre']
            else:
                nombre = obj.nombre

            if 'apellido' in form.initial:
                apellido = form.cleaned_data['apellido']
            else:
                apellido = obj.apellido

            if 'email' in form.initial:
                email = form.cleaned_data['email']
            else:
                email = obj.nombre

            usuario, creado = User.objects.update_or_create(username=email,
                                                            defaults={'username': obj.email,
                                                                      'first_name': obj.jurado[:30],
                                                                      'email': obj.email})
            if creado:
                password = User.objects.make_random_password()
                usuario.set_password(password)
            obj.usuario = usuario

        super(ProfesionalAdmin, self).save_model(request, obj, form, change)


@admin.register(Administrativo)
class AdministrativoAdmin(admin.ModelAdmin):
    readonly_fields = ('usuario',)

    def save_model(self, request, obj, form, change):
        from django.contrib.auth.models import User
        if 'nombre' in form.changed_data or 'apellido' in form.changed_data or 'email' in form.changed_data:
            if 'nombre' in form.initial:
                nombre = form.cleaned_data['nombre'][:30]
            else:
                nombre = obj.nombre

            if 'apellido' in form.initial:
                apellido = form.cleaned_data['apellido'][:30]
            else:
                apellido = obj.apellido

            if 'email' in form.initial:
                email = form.cleaned_data['email']
            else:
                email = obj.nombre

            usuario, creado = User.objects.update_or_create(username=email,
                                                            defaults={'username': email,
                                                                      'first_name': nombre,
                                                                      'last_name': apellido,
                                                                      'email': email})
            if creado:
                password = User.objects.make_random_password()
                usuario.set_password(password)
                usuario.is_active = True
                usuario.is_staff = True
                usuario.save()
            obj.usuario = usuario

        super(AdministrativoAdmin, self).save_model(request, obj, form, change)

