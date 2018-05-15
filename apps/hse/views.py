from django.shortcuts import render, get_object_or_404
from .models import StuffAll, StuffInside, Guest
from django.views import generic
from django.db.models import Q

# Create your views here.

def employees(par):
    if par == 'all':
        return StuffAll.objects.all().count()
    elif par == 'theoric':
        #returns employee list who are on vacation
        stuff_on_vacation = StuffAll.objects.filter(on_vacation = True)
        # exclude from the StuffInside list employees who are on vacation and left the workplace
        return StuffInside.objects.exclude(Q(empid__in=stuff_on_vacation) | Q( office_left = True)).count()
    elif par == 'unknown':
        #returns employee list who are on vacation
        stuff_on_vacation = StuffAll.objects.filter(on_vacation = True)
        # exclude from the StuffInside list employees who are on vacation and left the workplace
        stuff_left_and_vacation = StuffInside.objects.exclude(Q(empid__in=stuff_on_vacation) | Q( office_left = True)).values_list('empid', flat = True)
        # StuffInside list (set) employees who are theoretically on vacation and left the workplace, ONLY empid.
        empInsideList_theory = set([StuffAll.objects.values_list('empid', flat = True).get(pk=i) for i in  stuff_left_and_vacation])
        # return employee list who are checked in an entrance of the workplace
        checked = StuffInside.objects.filter(office_entered = True).values_list('empid', flat = True)
        # StuffInside list (set) employees who are entered to the workplace, ONLY empid.
        empInsideList_fact  = set([StuffAll.objects.values_list('empid', flat = True).get(pk=i) for i in  checked])
        unknown_difference = (empInsideList_theory - empInsideList_fact)
        return StuffAll.objects.filter(empid__in = unknown_difference).count()
    else:
        return None

def index(request):
    template = "hse/index.html"
    stuff = StuffAll.objects.all()
    context_data = {"stuff": stuff}
    return render(request, template, context_data)

class StuffListView(generic.ListView):
    model = StuffAll
    paginate_by = 30
    def get_context_data(self, **kwargs):
        context = super(StuffListView, self).get_context_data(**kwargs)
        context['cnt'] = StuffAll.objects.all().count()
        return context

class StuffDetailView(generic.DetailView):
    model = StuffInside

    def get_context_data(self, **kwargs):
        context = super(StuffDetailView, self).get_context_data(**kwargs)
        context['rescued_count'] = StuffInside.objects.filter(Q(assembly_point_checked = True) & Q(office_entered = True)).count()
        context['in_count'] = StuffInside.objects.filter(Q(assembly_point_checked = False) & Q(office_entered = True)).count()
        context['unknown_count'] = employees('unknown')
        context['all_employee_count'] = employees('all')
        context['theoric_employee_count'] = employees('theoric')
        return context

class StuffUnknownDetailView(generic.DetailView):
    model = StuffAll

    def get_context_data(self, **kwargs):
        context = super(StuffUnknownDetailView, self).get_context_data(**kwargs)
        context['rescued_count'] = StuffInside.objects.filter(Q(assembly_point_checked = True) & Q(office_entered = True)).count()
        context['in_count'] = StuffInside.objects.filter(Q(assembly_point_checked = False) & Q(office_entered = True)).count()
        context['unknown_count'] = employees('unknown')
        context['all_employee_count'] = employees('all')
        context['theoric_employee_count'] = employees('theoric')
        return context

class StuffRescuedListView(generic.ListView):
    model = StuffInside
    paginate_by = 30

    def get_queryset(self):
        return StuffInside.objects.filter(Q(assembly_point_checked = True) & Q(office_entered = True)) # return list who is in the assembly point

    def get_context_data(self, **kwargs):
        context = super(StuffRescuedListView, self).get_context_data(**kwargs)
        context['rescued_count'] = StuffInside.objects.filter(Q(assembly_point_checked = True) & Q(office_entered = True)).count()
        context['in_count'] = StuffInside.objects.filter(Q(assembly_point_checked = False) & Q(office_entered = True)).count()
        context['unknown_count'] = employees('unknown')
        context['all_employee_count'] = employees('all')
        context['theoric_employee_count'] = employees('theoric')
        return context

class StuffInListView(generic.ListView):
    model = StuffInside
    paginate_by = 30
    context_object_name = 'stuffin'
    template_name = 'hse/stuffin.html' # use same model for the different views

    def get_queryset(self):
        return StuffInside.objects.filter(Q(assembly_point_checked = False) & Q(office_entered = True)) # return list who is in the assembly point

    def get_context_data(self, **kwargs):
        context = super(StuffInListView, self).get_context_data(**kwargs)
        context['rescued_count'] = StuffInside.objects.filter(Q(assembly_point_checked = True) & Q(office_entered = True)).count()
        context['in_count'] = StuffInside.objects.filter(Q(assembly_point_checked = False) & Q(office_entered = True)).count()
        context['unknown_count'] = employees('unknown')
        context['all_employee_count'] = employees('all')
        context['theoric_employee_count'] = employees('theoric')
        return context

class StuffUnknownListView(generic.ListView):
    model = StuffAll
    paginate_by = 30
    context_object_name = 'stuffunknown'
    template_name = 'hse/stuffunknown.html' # use same model for the different views

    def get_queryset(self):
        #returns employee list who are on vacation
        stuff_on_vacation = StuffAll.objects.filter(on_vacation = True)

        # exclude from the StuffInside list employees who are on vacation and left the workplace
        stuff_left_and_vacation = StuffInside.objects.exclude(Q(empid__in=stuff_on_vacation) | Q( office_left = True)).values_list('empid', flat = True)

        # StuffInside list (set) employees who are theoretically on vacation and left the workplace, ONLY empid.
        empInsideList_theory = set([StuffAll.objects.values_list('empid', flat = True).get(pk=i) for i in  stuff_left_and_vacation])

        # return employee list who are checked in an entrance of the workplace
        checked = StuffInside.objects.filter(office_entered = True).values_list('empid', flat = True)

        # StuffInside list (set) employees who are entered to the workplace, ONLY empid.
        empInsideList_fact  = set([StuffAll.objects.values_list('empid', flat = True).get(pk=i) for i in  checked])

        # get a count of employees with an unclear status
        unknown_difference = (empInsideList_theory - empInsideList_fact)
        return StuffAll.objects.filter(empid__in = unknown_difference)

    def get_context_data(self, **kwargs):
        context = super(StuffUnknownListView, self).get_context_data(**kwargs)
        context['rescued_count'] = StuffInside.objects.filter(Q(assembly_point_checked = True) & Q(office_entered = True)).count()
        context['in_count'] = StuffInside.objects.filter(Q(assembly_point_checked = False) & Q(office_entered = True)).count()
        context['unknown_count'] = employees('unknown')
        context['all_employee_count'] = employees('all')
        context['theoric_employee_count'] = employees('theoric')
        return context
