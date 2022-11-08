from django.db.models import QuerySet, Manager, Q


class DoctorQuerySet(QuerySet):
    def by_service(self):
        return self.filter()


class DoctorManager(Manager.from_queryset(DoctorQuerySet)):
    pass
