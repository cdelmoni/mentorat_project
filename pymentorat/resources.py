from django.core.exceptions import ObjectDoesNotExist

from import_export import resources
from .models import Discipline, Student, Teacher

class DisciplineResource(resources.ModelResource):
    class Meta:
        model = Discipline


class StudentResource(resources.ModelResource):
    """ Class for importing and exporting Students data """

    def get_or_init_instance(self, instance_loader, row):
        """ For existing item, get the object in database based on the id_OD and fill the id with the primary key """

        id_OD = row["id_OD"]
        try:
            obj = Student.objects.get(id_OD=id_OD)

            row["id"]=obj.pk

        except ObjectDoesNotExist:
            pass

        return super(StudentResource,self).get_or_init_instance(instance_loader, row)


    class Meta:
        model = Student
        skip_unchanged = True
        report_skipped = True
        fields = (
            'id',
            'id_OD',
            'name',
            'vorname',
            'classe',
            'email',
        )

        export_order = fields

#        import_id_fields = ('id_OD')


class TeacherResource(resources.ModelResource):
    """ Class for importing and exporting Teacher data """

    def get_or_init_instance(self, instance_loader, row):
        """ For existing item, get the object in database based on the id_OD and fill the id with the primary key """
        id_OD = row["id_OD"]
        try:
            obj = Teacher.objects.get(id_OD=id_OD)

            row["id"]=obj.pk

        except ObjectDoesNotExist:
            pass

        return super(TeacherResource,self).get_or_init_instance(instance_loader, row)


    class Meta:
        model = Teacher
        skip_unchanged = True
        report_skipped = True
        fields = (
            'id',
            'id_OD',
            'name',
            'vorname'
        )

        export_order = fields

