from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.urls import reverse_lazy
from metaord.models import Order, MetaordSettings, STATUS_CHOICES_AND_CLASS
from metaord.utils.view import ExtraContext
from metaord.utils.decorators import group_required, class_decorator
from django.contrib.auth.decorators import user_passes_test


@class_decorator(group_required("chief", login_url="/login/"))
class SettingsUpdate(UpdateView):
    model = MetaordSettings
    template_name = "metaord/settings.html"
    fields = "__all__"
    success_url = reverse_lazy("chief:projects")
    success_message = "Настройки успешно изменены"

    def get_object(self, queryset=None):
        obj = MetaordSettings.objects.all().first()
        return obj

def page_not_found(request):
    response = render_to_response('metaord/404.html', context=RequestContext(request))
    response.status_code = 404
    return response

def error_view(request):
    response = render_to_response('metaord/500.html', context=RequestContext(request))
    response.status_code = 500
    return response


class OrderList(ExtraContext, ListView):
    model = Order
    extra_context = {"order_statuses": STATUS_CHOICES_AND_CLASS}

    def get_context_data(self, **kwargs):
        context = super(OrderList, self).get_context_data(**kwargs)
        context["order_status"] = self.request.GET.get("order_status")
        return context

    def get_queryset(self):
        status = self.request.GET.get("order_status")
        if status is None:
            return Order.objects.all()
        else:
            return Order.objects.filter(status=status)

class OrderDetail(DetailView):
    model = Order

class OrderCreate(CreateView):
    model = Order
    fields = ["project", "post_date", "status"]

class OrderDelete(DeleteView):
    model = Order
    success_url = '/deleted'