# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import views
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import action

from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, IsAuthenticated
from api.permissions import IsOwnerOrReadOnly, IsSelfOrStaff

from api.serializers import UserSerializer, WorkoutSerializer

from MyUser.models import User, Workout
from django.shortcuts import get_object_or_404, render

from django.db.models import Q

from django.utils import timezone
import datetime

from measurement.measures import Weight


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        """
        Filter objects so a user only sees his own stuff.
        If user is admin, let him see all.
        """
        qs = User.objects.all().order_by('-pk')
        query = self.request.GET.get('q')
        if query is not None:
            qs = qs.filter(
                Q(email__icontains=query) |
                Q(display_name__icontains=query)
            ).distinct()
        return qs


class WorkoutsViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutSerializer
    permission_classes = (IsAuthenticated,)  # Should also be owner

    def get_queryset(self):
        """
        Filter objects so a user only sees his own stuff.
        If user is admin, let him see all.
        """
        user = self.request.user
        qs = user.workouts.all().order_by('-pk')
        return qs

    @action(detail=False)
    def today(self, request):
        user = self.request.user
        qs = user.workouts.filter(date__day=timezone.now().day).order_by('-pk')
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ExercisesViewSet(viewsets.ModelViewSet):
    """docstring for ExercisesViewSet."""
    def __init__(self, arg):
        super(ExercisesViewSet, self).__init__()
        self.arg = arg
