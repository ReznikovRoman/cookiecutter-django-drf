from django.db.models import QuerySet


class CustomDeleteQueryset(QuerySet):
    def delete(self):
        # have to call .delete() method when deleting a Realty queryset (e.g. on the Admin panel)
        for obj in self:
            obj.delete()
