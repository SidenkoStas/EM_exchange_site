from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from .models import Ad
from .forms import CreateAdForm

class HomeView(ListView):
    template_name = "ads/home.html"
    queryset = Ad.objects.all()
    context_object_name = "ads"
    paginate_by = 10

class ProfileView(ListView):
    template_name = "ads/profile.html"
    context_object_name = "ads"
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        queryset = Ad.objects.filter(user=user)
        return queryset

class AdCreateView(CreateView):
    template_name = "ads/create.html"
    form_class = CreateAdForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class AdDetailView(DetailView):
    queryset = Ad.objects.all()
    template_name = "ads/detail.html"
    context_object_name = "ad"

class AdUpdateView(UpdateView):
    queryset = Ad.objects.all()
    template_name = "ads/update.html"
    form_class = CreateAdForm

def delete_ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    ad.delete()
    return render(
        request, "ads/delete.html", {"title": ad.title}
    )
