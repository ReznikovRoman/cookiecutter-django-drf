from django.db.models import QuerySet


class CustomDeleteQueryset(QuerySet):
    def delete(self):
        # call .delete() on each object when deleting a queryset (e.g. on the Admin panel)
        for obj in self:
            obj.delete()
