from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from .models import Ad, Category
from .forms import CreateAdForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

class HomeView(ListView):
    template_name = "ads/home.html"
    queryset = Ad.objects.all()
    context_object_name = "ads"
    paginate_by = 10
    ordering = ["-created_at"]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context["category"] = Category.objects.all()
        context["condition"] = Ad.Condition
        # context["condition"] = ((c.label, c.value) for c in Ad.Condition)
        return context

class ProfileView(LoginRequiredMixin, ListView):
    template_name = "ads/profile.html"
    context_object_name = "ads"
    paginate_by = 10
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        queryset = Ad.objects.filter(user=user)
        return queryset

class AdCreateView(LoginRequiredMixin, CreateView):
    template_name = "ads/create.html"
    form_class = CreateAdForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class AdDetailView(LoginRequiredMixin, DetailView):
    queryset = Ad.objects.all()
    template_name = "ads/detail.html"
    context_object_name = "ad"

    def get_object(self, queryset=None):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied
        return obj

class AdUpdateView(LoginRequiredMixin, UpdateView):
    queryset = Ad.objects.all()
    template_name = "ads/update.html"
    form_class = CreateAdForm

    def get_object(self, queryset=None):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied
        return obj

def delete_ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if request.user != ad.user:
        return render(request, "403.html")
    ad.delete()
    return render(
        request, "ads/delete.html", {"title": ad.title}
    )

class AdListByFilter(ListView):
    template_name = "ads/home.html"
    context_object_name = "ads"

    def get_queryset(self):
        filter_name = self.kwargs["filter"]
        try:
            filter_name = Ad.Condition[filter_name] or filter_name
        except:
            pass
        queryset = Ad.objects.filter(
            Q(category__title=filter_name) |
            Q(condition=filter_name)
        )
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context["category"] = Category.objects.all()
        context["condition"] = Ad.Condition
        return context