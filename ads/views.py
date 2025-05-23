from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from .models import Ad, Category, ExchangeProposal
from .forms import CreateAdForm, ExchangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models.functions import Lower

class HomeView(ListView):
    """
    Отображение списка объявлений с возможностью фильтрации.
    """
    template_name = "ads/home.html"
    queryset = Ad.objects.all()
    context_object_name = "ads"
    paginate_by = 10
    ordering = ("-created_at",)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context["category"] = Category.objects.all()
        context["condition"] = Ad.Condition
        filtering = self.kwargs.get("filtering")
        if filtering in Ad.Condition:
            context["filtering"] = Ad.Condition[filtering].label
        else:
            context["filtering"] = filtering
        return context

    def get_queryset(self):
        if self.kwargs.get("filtering"):
            filter_name = self.kwargs["filtering"]
            try:
                filter_name = Ad.Condition[filter_name].label
            except KeyError:
                pass
            queryset = Ad.objects.filter(
                Q(category__title=filter_name) |
                Q(condition=filter_name)
            )
        else:
            queryset = super().get_queryset()
        return queryset

class ProfileView(LoginRequiredMixin, ListView):
    """
    Отображение всех объявлений пользователя.
    """
    template_name = "ads/profile.html"
    context_object_name = "ads"
    paginate_by = 10
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        queryset = Ad.objects.filter(user=user)
        return queryset

class AdCreateView(LoginRequiredMixin, CreateView):
    """
    Создание объявления.
    """
    template_name = "ads/create.html"
    form_class = CreateAdForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class AdDetailView(DetailView):
    """
    Просмотр объявления отдельно.
    """
    queryset = Ad.objects.all()
    template_name = "ads/detail.html"
    context_object_name = "ad"

class AdUpdateView(LoginRequiredMixin, UpdateView):
    """
    Обновление объявления.
    """
    queryset = Ad.objects.all()
    template_name = "ads/update.html"
    form_class = CreateAdForm

    def get_object(self, queryset=None):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied
        return obj

def delete_ad(request, pk):
    """
    Уцдаление объявления.
    """
    ad = get_object_or_404(Ad, pk=pk)
    if request.user != ad.user:
        return render(request, "403.html")
    ad.delete()
    return render(
        request, "ads/delete.html", {"title": ad.title}
    )

class SearchingView(ListView):
    """
    Поиск по заголовку и в названии.
    Выдаёт список объявлений.
    """
    template_name = "ads/searching.html"
    context_object_name = "ads"
    paginate_by = 10
    ordering = ("-created_at",)

    def get_queryset(self):
        searching = self.request.GET.get("searching")
        queryset = Ad.objects.annotate(
            lower_title = Lower("title"),
            lower_description = Lower("description")
        ).filter(
            Q(lower_title__icontains=searching.lower()) |
            Q(lower_description__icontains=searching.lower())
        )
        return queryset

def exchange_view(request, pk):
    """
    Создание запроса на обмен.
    """
    ad = Ad.objects.get(pk=pk)
    user = request.user
    if request.method == "POST":
        form = ExchangeForm(request.POST, user=user)
        if form.is_valid():
            exchange = form.save(commit=False)
            exchange.ad_receiver = ad
            exchange.save()
            return render(request, "ads/exchange_success.html")
    else:
        form = ExchangeForm(user=user)
    return render(
        request, "ads/exchange.html",
        {"form": form, "ad": ad}
    )

class ExchangeListView(ListView):
    """
    Список всех запросов на обмен.
    """
    template_name = "ads/list_exchange.html"
    context_object_name = "ads"
    paginate_by = 10
    ordering = ("-created_at", )

    def get_queryset(self):
        user = self.request.user
        filt = self.kwargs.get("ex_filter")
        if filt:
            if filt == "sender":
                queryset = ExchangeProposal.objects.filter(
                    ad_sender__user=user
                )
            elif filt == "receiver":
                queryset = ExchangeProposal.objects.filter(
                    ad_receiver__user=user
                )
            else:
                queryset = ExchangeProposal.objects.filter(
                    Q(ad_sender__user=user) |
                    Q(ad_receiver__user=user)
                ).filter(status=filt)
        else:
            queryset = ExchangeProposal.objects.filter(
                Q(ad_sender__user=user) |
                Q(ad_receiver__user=user)
            )
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context["status"] = ExchangeProposal.Status
        return  context