from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from models import Refuge, Dog, Vaccine
from forms import RefugeForm, DogForm

from dogapp.forms import SignUpForm


# Create your views here.

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/dogapp')
    else:
        form = SignUpForm()
    return render(request, 'dogapp/signup.html', {'form': form})


class RefugeDetail(DetailView):
    model = Refuge
    template_name = 'dogapp/refuge_detail.html'

    def get_context_data(self, **kwargs):
        context = super(RefugeDetail, self).get_context_data(**kwargs)
        return context


class RefugeCreate(CreateView):
    model = Refuge
    template_name = 'dogapp/form.html'
    form_class = RefugeForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(RefugeCreate, self).form_valid(form)


class DogCreate(CreateView):
    model = Dog
    template_name = 'dogapp/form.html'
    form_class = DogForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.refuge = Refuge.objects.get(id=self.kwargs['pk'])
        return super(DogCreate, self).form_valid(form)
