from django.db import models
from django.urls import reverse

# Create your models here.

class Country(models.Model):
    """
    List of countries and their cities where company is located
    """
    city = models.CharField( null = False, blank = False, max_length = 30, help_text = "Name of the city")
    country = models.CharField( null = False, blank = False, max_length = 30, help_text = "Name of the country")

    def __str__(self):
        return "%s, %s" % (self.city, self.country)

class StuffAll(models.Model):
    """
    All information about company stuff.
    """
    empid = models.IntegerField(default = 0, help_text = "Employee ID")
    name = models.CharField(blank = False, max_length = 50, help_text = "Full name")
    position = models.CharField(blank = True, default = '', max_length = 120, help_text = "Position of the employee")
    department = models.CharField(default = '', blank = True, max_length = 120, help_text = "Department name of the employee")
    department_id = models.CharField(default = '', blank = True, max_length = 2, help_text = "Department ID of the employee")
    email = models.EmailField( blank = True, default = '', help_text = "E-mail address")
    mobile  = models.CharField(default = '',blank = True, max_length = 50, help_text = "Mobile number")
    phone = models.CharField(default = '', blank = True, max_length = 50, help_text = "Phone number")
    birth_date = models.DateField( null = True, blank = True, auto_now = False, help_text = "Birth Date")
    start_date = models.DateField( null = True, blank = True, auto_now = False, help_text = "Employee's start date in the company")
    building = models.CharField(default = '', blank = True, max_length = 20, help_text = "Building name or number where employee is sitting")
    city = models.ForeignKey(Country, help_text = "Name of the city where employee is working", on_delete=models.CASCADE)
    floor = models.SmallIntegerField(null = True, blank = True, help_text = "The Floor number where employee's room located")

    workplace_name = (
                (' ',' '),
                ('po','Plant Office'),
                ('co','City Office'),
            )

    workplace = models.CharField(max_length = 2, choices = workplace_name, blank = True, default = ' ', help_text = "Workplace of the employee, for instance, Plant, City Office ect.")

    genre_types = (
                (' ',' '),
                ('m','Male'),
                ('f','Female'),
            )
    genre = models.CharField(max_length = 1, choices = genre_types, blank = True, default = ' ', help_text = "Employee genre")
    profilepic = models.ImageField(null = True, max_length = 100, help_text = "Profile picture")
    on_vacation = models.BooleanField(default = False, help_text = "True - employee is on vacation, False - employee is not on vacation")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        """
        Represent name of the employeers as a Model object
        """
        return "%s" % (self.empid)

    def get_absoulte_url(self):
        """
        Return the URL to access employeers detiled information page
        """
        return reverse('stuff-detail', args=[str(self.empid)])

class Guest(models.Model):
    """
    Information about company's guests
    """
    badge_id = models.CharField(default='', max_length = 30, blank = True, help_text = "Guest badge ID given temporarily by the company.")
    name = models.CharField(blank = False, max_length = 50, help_text = "Guest full name")
    entry_date = models.DateTimeField(auto_now = False, help_text = "Guest's entry date and time")
    exit_date = models.DateTimeField(auto_now = False, help_text = "Guest's exit date and time")
    guest_company = models.CharField(default = '', max_length = 50, blank = True, help_text = "Company name of the guest")
    guest_meet = models.CharField(default = '', max_length = 150, blank = True, help_text = "Employee name(s) who will meet the guest(s).")
    guest_vehicle_num = models.CharField(default = '', max_length = 30, blank = True, help_text = "Car vehicle number of the guest")
    office_entered = models.BooleanField(default = False, help_text = "True - if guest entered to the workplace, else False")

    class Meta:
        ordering  = ["name"]

    def __str__(self):
        """
        Represent name of the guests
        """
        return "%s, %s, %s" % (self.name,self.guest_meet, self.entry_date)

    def get_absoulte_url(self):
        """
        Return the URL to access guests detail information page
        """
        return reverse('guest-detail', args=[str(self.id)])

class StuffInside(models.Model):
    """
    Information about employees who are registered as in the workplace.
    """
    empid = models.ForeignKey(StuffAll, help_text = "Employee ID", on_delete=models.CASCADE)
    name = models.CharField(blank = False, max_length = 50, help_text = "Full name")
    position = models.CharField(blank = True, default = '', max_length = 120, help_text = "Position of the employee")
    department = models.CharField(default = '', blank = True, max_length = 120, help_text = "Department name of the employee")
    department_id = models.CharField(default = '', blank = True, max_length = 2, help_text = "Department ID of the employee")
    email = models.EmailField( blank = True, default = '', help_text = "E-mail address")
    mobile  = models.CharField(default = '',blank = True, max_length = 50, help_text = "Mobile number")
    phone = models.CharField(default = '', blank = True, max_length = 50, help_text = "Phone number")
    birth_date = models.DateField( null = True, blank = True, auto_now = False, help_text = "Birth Date")
    start_date = models.DateField( null = True, blank = True, auto_now = False, help_text = "Employee's start date in the company")
    building = models.CharField(default = '', blank = True, max_length = 20, help_text = "Building name or number where employee is sitting")
    city = models.ForeignKey(Country, help_text = "Employee ID number",on_delete=models.CASCADE)
    floor = models.SmallIntegerField(null = True, blank = True, help_text = "The Floor number where employee's room located")

    genre_types = (
                (' ',' '),
                ('m','Male'),
                ('f','Female'),
            )
    genre = models.CharField(max_length = 1, choices = genre_types, blank = True, default = ' ', help_text = "Employee genre")
    profilepic = models.ImageField(null = True, max_length = 100, help_text = "Profile picture")
    # employee vacation information mentioned in the StuffAll table
    #on_vacation = models.BooleanField(default = False, help_text = "True - employee is on vacation, False - employee is not on vacation")
    office_entered = models.BooleanField(default = False, help_text = "True - if employee entered to the workplace, else False (value office_left)")
    office_left = models.BooleanField(default = False, help_text = "True - if employee has left the workplace, else False (value office_entered)")
    left_time = models.DateTimeField(null = True, blank = True, auto_now = False, help_text = "Date and time when employee left the workplace")
    assembly_point_checked = models.BooleanField(default = False, help_text = "True - employee checked him(her)self in the assembly point, else False")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        """
        Represent name of the employeers as a Model object
        """
        return "%s, %s, %s" % (self.name,self.city, self.pk)

    def get_absoulte_url(self):
        """
        Return the URL to access employeers detiled information page
        """
        return reverse('stuff-detail', args=[str(self.empid)])
