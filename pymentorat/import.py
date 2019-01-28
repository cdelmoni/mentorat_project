import tablib
from import_export import resources

from .models import Student

student_resource = resources.modelresource_factory(model=Student)()
dataset = tablib.Dataset()
