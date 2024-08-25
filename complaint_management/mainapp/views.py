from django.shortcuts import render, redirect, get_object_or_404
from .models import Complaint, Comment
from django.contrib.auth.models import User
from .forms import CommentForm
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView, DeleteView, DetailView, ListView
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


# Create your views here.

class IndexView(TemplateView):
    template_name = "index.html"


class ComplaintListView(ListView):
    model = Complaint
    template_name = "index.html"

    def get_queryset(self):
        return Complaint.objects.filter(created_at__lte=timezone.now()).order_by("-created_at")


class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = "user_create.html"
    success_url = reverse_lazy("mainapp:login")

class ComplaintCreateView(LoginRequiredMixin, CreateView):
    model = Complaint
    fields = ("title", "description", "category", "status")
    template_name = 'create_complaint.html'
    success_url = reverse_lazy("mainapp:index")

    def form_valid(self, form):
        # Set the user to the currently logged-in user
        form.instance.user = self.request.user
        return super().form_valid(form)

class ComplaintDetailView(DetailView):
    model = Complaint
    template_name = "complaint_detail.html"



class ComplaintDeleteView(LoginRequiredMixin, DeleteView):
    model = Complaint
    template_name = "complaint_delete.html"
    success_url=reverse_lazy("mainapp:index")

@login_required
def add_comment_to_complaint(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.complaint = complaint
            comment.user = request.user  # Automatically set the user field
            comment.save()
            return redirect('mainapp:complaint_detail', pk=complaint.pk)
    else:
        form = CommentForm()
    
    return render(request, 'comment_form.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("mainapp:index"))



def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:

            if user.is_active:
                login(request, user=user)
                return HttpResponseRedirect(reverse("mainapp:index"))
            
            else:
                return HttpResponse("User is not active!")
            
        else:
            print("Someone tried to log in and failed!")
            print("username: " + username + "password: " + password)
            return HttpResponse("Invalid login details!")
        
    else:
        return render(request, "login.html", {})




