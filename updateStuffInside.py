import os
# Django variables
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Evacuation.settings")
#from django.core.management import execute_from_command_line
import django
django.setup()
from apps.hse.models import StuffAll, Country, StuffInside

stuffall = StuffAll.objects.all()
emp_city = Country.objects.get(city="Baku")

for st in stuffall:
    emp_id = StuffAll.objects.get(empid=st.empid)
    inside = StuffInside(
                    empid = emp_id, name = st.name, position = st.position, department  = st.department,
                    department_id = st.department_id, email = st.email, mobile = st.mobile, phone = st.phone,
                    birth_date = st.birth_date, start_date = st.start_date, building  = st.building,
                    city = emp_city, floor = st.floor, genre = st.genre, profilepic = st.profilepic
                    )
    inside.save()
