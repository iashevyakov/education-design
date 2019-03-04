# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=60, unique=True, verbose_name='Название')


class Person(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=False, blank=False, verbose_name='Роль')
    name = models.CharField(max_length=60, verbose_name='ФИО')


class Module(models.Model):
    type = models.CharField(max_length=20)
    info = models.TextField(verbose_name='Информация', null=True, blank=True)


class Step(models.Model):
    module = models.ForeignKey(Module, null=False, blank=False, verbose_name='Модуль', on_delete=models.CASCADE)
    type = models.CharField(max_length=30, null=True, blank=True, verbose_name='Тип')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    content = models.TextField(null=True, blank=True, verbose_name='Контент')


class ModuleDependency(models.Model):
    module = models.ForeignKey(Module, related_name='module_dependents', null=False, blank=False, verbose_name='Модуль',
                               on_delete=models.CASCADE)
    dependent_module = models.ForeignKey(Module, null=False, blank=False, verbose_name='Зависимый модуль',
                                         on_delete=models.CASCADE, related_name='module_dependencies')

    class Meta:
        unique_together = (('module', 'dependent_module'),)


class PersonModule(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=False, blank=False, verbose_name='Человек')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, null=False, blank=False, verbose_name='Модуль')
    passed = models.BooleanField(verbose_name='Пройден')

    class Meta:
        unique_together = (('person', 'module'),)


class Competence(models.Model):
    name = models.CharField(max_length=60, unique=True, verbose_name='Название', null=False, blank=False)
    description = models.TextField(null=True, blank=True, verbose_name='Описание')


class CompetenceLevel(models.Model):
    competence = models.ForeignKey(Competence, null=False, blank=False, verbose_name='Компетенция')
    level = models.IntegerField(null=False, blank=False, verbose_name='Уровень')
    score_to_pass = models.IntegerField(null=False, blank=False, verbose_name='Оценка для сдачи')
    function_to_evaluate = models.CharField(max_length=200, null=False, blank=False, verbose_name='Функция оценивания')

    class Meta:
        unique_together = (('competence', 'level'),)


class CompetenceLevelScale(models.Model):
    competence_level_1 = models.ForeignKey(CompetenceLevel, null=False, blank=False,
                                           verbose_name='Уровень компетенции 1', related_name='lower_levels')
    competence_level_2 = models.ForeignKey(CompetenceLevel, null=False, blank=False,
                                           verbose_name='Уровень компетенции 2', related_name='higher_levels')
    score = models.IntegerField(null=False, blank=False,
                                verbose_name='Оценка по уровню 1 для получения уровня 2')

    class Meta:
        unique_together = (('competence_level_1', 'competence_level_2'),)


class RoleCompetenceLevel(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=False, blank=False, verbose_name='Роль')
    competence_level = models.ForeignKey(CompetenceLevel, null=False, blank=False, on_delete=models.CASCADE,
                                         verbose_name='Уровень компетенции')
    weight = models.IntegerField(null=True, blank=True, verbose_name='Вес компетенции для роли')

    class Meta:
        unique_together = (('role', 'competence_level'),)


class ModuleCompetenceLevel(models.Model):
    module = models.ForeignKey(Module, null=False, blank=False, verbose_name='Модуль')
    competence_level = models.ForeignKey(CompetenceLevel, null=False, blank=False, verbose_name='Уровень компетенции')

    class Meta:
        unique_together = (('module', 'competence_level'),)


TYPES = (
    ('actiity_exam', 'ACTIVITY_EXAM'),
    ('tasks', 'TASKS')
)


class PersonCompetenceLevelChoice(models.Model):
    person = models.ForeignKey(Person, null=False, blank=False, verbose_name='Человек')
    competence_level = models.ForeignKey(CompetenceLevel, null=False, blank=False, verbose_name='Уровень компетенции')

    class Meta:
        unique_together = (('person', 'competence_level'),)


class PersonCompetenceLevel(models.Model):
    person = models.ForeignKey(Person, null=False, blank=False, verbose_name='Человек')
    competence_level = models.ForeignKey(CompetenceLevel, null=False, blank=False, verbose_name='Уровень компетенции')
    score = models.IntegerField()
    type = models.CharField(choices=TYPES, default=TYPES[1][0], max_length=15)

    class Meta:
        unique_together = (('person', 'competence_level', 'type'),)


class ActivityExam(models.Model):
    competence_level = models.ForeignKey(CompetenceLevel, null=False, blank=False, on_delete=models.CASCADE,
                                         verbose_name='Уровень кометенции')
    task = models.TextField(null=False, blank=False, verbose_name='Текст задания')
    score_to_pass = models.IntegerField(null=False, blank=False, verbose_name='Оценка для сдачи')

    class Meta:
        unique_together = (('competence_level', 'task'),)


class Task(models.Model):
    competence_level = models.ForeignKey(CompetenceLevel, null=False, blank=False, verbose_name='Уровень компетенции')
    module = models.ForeignKey(Module, null=False, blank=False, verbose_name='Модуль')
    task_text = models.TextField(null=False, blank=False, verbose_name='Текст задания')
    answer_text = models.TextField(null=True, blank=True, verbose_name='Ответ на задание')
    score = models.IntegerField(null=True, blank=True, verbose_name='Максимальный балл за задание')
    weight = models.IntegerField(null=True, blank=True, verbose_name='Вес задания')

    class Meta:
        unique_together = (('competence_level', 'module', 'task_text'),)


class TaskResult(models.Model):
    person = models.ForeignKey(Person, null=False, blank=False, verbose_name='Человек')
    task = models.ForeignKey(Task, null=False, blank=False, verbose_name='Задание')
    score = models.IntegerField(null=False, blank=False, verbose_name='Оценка')

    class Meta:
        unique_together = (('person', 'task'),)
