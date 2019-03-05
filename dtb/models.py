# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=60, unique=True, verbose_name='Название')

    def __str__(self):
        return self.name


class Person(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=False, blank=False, verbose_name='Роль')
    name = models.CharField(max_length=60, verbose_name='ФИО')

    def __str__(self):
        return self.name + ' | ' + self.role.name


class Module(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    type = models.CharField(max_length=20, verbose_name='Тип')
    info = models.TextField(verbose_name='Информация', null=True, blank=True)

    def __str__(self):
        return self.name + ' | ' + self.type

    class Meta:
        unique_together = (('name', 'type'),)


class Step(models.Model):
    module = models.ForeignKey(Module, null=False, blank=False, verbose_name='Модуль', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name='Название')
    type = models.CharField(max_length=30, null=True, blank=True, verbose_name='Тип')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    content = models.TextField(null=True, blank=True, verbose_name='Контент')

    def __str__(self):
        return self.name + '|' + self.type

    class Meta:
        unique_together = (('module', 'name', 'type'),)


class ModuleDependency(models.Model):
    module = models.ForeignKey(Module, related_name='module_dependents', null=False, blank=False, verbose_name='Модуль',
                               on_delete=models.CASCADE)
    dependent_module = models.ForeignKey(Module, null=False, blank=False, verbose_name='Зависимый модуль',
                                         on_delete=models.CASCADE, related_name='module_dependencies')

    def __str__(self):
        return self.module.name + '->' + self.dependent_module.name

    class Meta:
        unique_together = (('module', 'dependent_module'),)


class PersonModule(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=False, blank=False, verbose_name='Человек')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, null=False, blank=False, verbose_name='Модуль')
    passed = models.BooleanField(verbose_name='Пройден')

    def __str__(self):
        return self.person.name + '|' + self.module.name

    class Meta:
        unique_together = (('person', 'module'),)


class Competence(models.Model):
    name = models.CharField(max_length=60, unique=True, verbose_name='Название', null=False, blank=False)
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return self.name


class CompetenceLevel(models.Model):
    competence = models.ForeignKey(Competence, null=False, blank=False, verbose_name='Компетенция')
    level = models.IntegerField(null=False, blank=False, verbose_name='Уровень')
    score_to_pass = models.IntegerField(null=False, blank=False, verbose_name='Оценка для сдачи')
    function_to_evaluate = models.CharField(max_length=200, null=False, blank=False, verbose_name='Функция оценивания')

    def __str__(self):
        return self.competence.name + '|' + str(self.level)

    class Meta:
        unique_together = (('competence', 'level'),)


class CompetenceLevelScale(models.Model):
    competence_level_1 = models.ForeignKey(CompetenceLevel, null=False, blank=False,
                                           verbose_name='Уровень компетенции 1', related_name='lower_levels')
    competence_level_2 = models.ForeignKey(CompetenceLevel, null=False, blank=False,
                                           verbose_name='Уровень компетенции 2', related_name='higher_levels')
    score = models.IntegerField(null=False, blank=False,
                                verbose_name='Оценка по уровню 1 для получения уровня 2')

    def __str__(self):
        return self.competence_level_1.competence.name + '(' + str(self.competence_level_1.level) + ')' + '[' + str(
            self.score) + '] - > ' + self.competence_level_2.competence.name + '(' + str(
            self.competence_level_2.level) + ')'

    class Meta:
        unique_together = (('competence_level_1', 'competence_level_2'),)


class RoleCompetenceLevel(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=False, blank=False, verbose_name='Роль')
    competence_level = models.ForeignKey(CompetenceLevel, null=False, blank=False, on_delete=models.CASCADE,
                                         verbose_name='Уровень компетенции')
    weight = models.IntegerField(null=True, blank=True, verbose_name='Вес компетенции для роли')

    def __str__(self):
        return self.role.name + ' | ' + self.competence_level.competence.name + '(' + str(
            self.competence_level.level) + ')'

    class Meta:
        unique_together = (('role', 'competence_level'),)


class ModuleCompetenceLevel(models.Model):
    module = models.ForeignKey(Module, null=False, blank=False, verbose_name='Модуль')
    competence_level = models.ForeignKey(CompetenceLevel, null=False, blank=False, verbose_name='Уровень компетенции')

    def __str__(self):
        return self.module.name + ' | ' + self.competence_level.competence.name + '(' + str(
            self.competence_level.level) + ')'

    class Meta:
        unique_together = (('module', 'competence_level'),)


TYPES = (
    ('actiity_exam', 'ACTIVITY_EXAM'),
    ('tasks', 'TASKS')
)


class PersonCompetenceLevelChoice(models.Model):
    person = models.ForeignKey(Person, null=False, blank=False, verbose_name='Человек')
    competence_level = models.ForeignKey(CompetenceLevel, null=False, blank=False, verbose_name='Уровень компетенции')

    def __str__(self):
        return self.person.name + ' | ' + self.competence_level.competence.name + '(' + str(
            self.competence_level.level) + ')'

    class Meta:
        unique_together = (('person', 'competence_level'),)


class PersonCompetenceLevel(models.Model):
    person = models.ForeignKey(Person, null=False, blank=False, verbose_name='Человек')
    competence_level = models.ForeignKey(CompetenceLevel, null=False, blank=False, verbose_name='Уровень компетенции')
    score = models.IntegerField()
    type = models.CharField(choices=TYPES, default=TYPES[1][0], max_length=15)

    def __str__(self):
        return self.person.name + ' | ' + self.competence_level.competence.name + '(' + str(
            self.competence_level.level) + ') = ' + str(self.score)

    class Meta:
        unique_together = (('person', 'competence_level', 'type'),)


class ActivityExam(models.Model):
    competence_level = models.ForeignKey(CompetenceLevel, null=False, blank=False, on_delete=models.CASCADE,
                                         verbose_name='Уровень кометенции')
    task = models.TextField(null=False, blank=False, verbose_name='Текст задания')
    score_to_pass = models.IntegerField(null=False, blank=False, verbose_name='Оценка для сдачи')

    def __str__(self):
        return self.competence_level.competence.name + '(' + str(
            self.competence_level.level) + ') | ' + str(self.task)

    class Meta:
        unique_together = (('competence_level', 'task'),)


class Task(models.Model):
    competence_level = models.ForeignKey(CompetenceLevel, null=False, blank=False, verbose_name='Уровень компетенции')
    module = models.ForeignKey(Module, null=False, blank=False, verbose_name='Модуль')
    task_text = models.TextField(null=False, blank=False, verbose_name='Текст задания')
    answer_text = models.TextField(null=True, blank=True, verbose_name='Ответ на задание')
    score = models.IntegerField(null=True, blank=True, verbose_name='Максимальный балл за задание')
    weight = models.IntegerField(null=True, blank=True, verbose_name='Вес задания')

    def __str__(self):
        return self.competence_level.competence.name + '(' + str(
            self.competence_level.level) + ') | ' + self.module.name + ' | ' + self.task_text

    class Meta:
        unique_together = (('competence_level', 'module', 'task_text'),)


class TaskResult(models.Model):
    person = models.ForeignKey(Person, null=False, blank=False, verbose_name='Человек')
    task = models.ForeignKey(Task, null=False, blank=False, verbose_name='Задание')
    score = models.IntegerField(null=False, blank=False, verbose_name='Оценка')

    def __str__(self):
        return self.person.name + ' | ' + self.task.task_text + ' = ' + str(self.score)

    class Meta:
        unique_together = (('person', 'task'),)
