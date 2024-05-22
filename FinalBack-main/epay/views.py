from chargily_epay_django.forms import FakePaymentForm
from chargily_epay_django.models import AbstractPayment
from chargily_lib.constant import PAYMENT_PAID, PAYMENT_CANCELED, PAYMENT_FAILED
from chargily_lib.invoice import new_invoice
from django.http import HttpResponseRedirect, HttpResponse, request, HttpRequest
from django.shortcuts import render

# Create your views here.
from chargily_epay_django.views import (
    CreatePaymentView,
    PaymentConfirmationView,
    PaymentObjectDoneView,
)
from django.views.generic import FormView
from django.views.generic.detail import BaseDetailView

from epay.forms import SponsorForm
from epay.models import Sponsor
class FakePaymentView(FormView, BaseDetailView):
    slug_field: str = "invoice_number"
    slug_url_kwarg = "invoice_number"
    template_name: str = "chargily_epay_django/fake-payment-view.html"
    form_class = FakePaymentForm
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        if "object" not in kwargs:
            kwargs["object"] = self.get_object()
        return super().get_context_data(**kwargs)

    def form_valid(self, form: FakePaymentForm):
        self.object = self.get_object()
        payment_status = form.data["status"]
        changed_data = form.changed_data
        changed_data = form.changed_data
        if payment_status == PAYMENT_PAID:
            self.object.payment_confirm()
        elif payment_status == PAYMENT_CANCELED:
            self.object.payment_canceled()
        elif payment_status == PAYMENT_FAILED:
            self.object.payment_failed()
        return HttpResponseRedirect(self.object.generate_back_url())

class FakeSponsor(FakePaymentView):
    model = Sponsor





class CreateSponsor(CreatePaymentView):
    payment_create_faild_url = ""
    template_name: str = "sponsor.html"
    form_class = SponsorForm
    def get(self, request, *args, **kwargs):
        query_params = self.kwargs['query_params']
        client, client_email, amount , mode= query_params.split('&')
        print(
            client, client_email, amount, mode
        )
        initial_data = {
            'client': client,
            'client_email': client_email,
            'amount': amount,
            'comment': '  ',
            'mode' : mode,
        }
        form = SponsorForm(initial=initial_data)  # Instantiate the form class
        form.fields['client'].widget.attrs['readonly'] = True
        form.fields['client_email'].widget.attrs['readonly'] = True
        form.fields['amount'].widget.attrs['readonly'] = True
        form.fields['mode'].widget.attrs['readonly'] = True
        context = {'form': form}  # Pass the form as context data
        return render(request, 'sponsor.html', context)
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            cleaned_data = form.cleaned_data
            print(cleaned_data.values())
            print(cleaned_data['amount'])
        else:
            print("Form is not valid")

        return super().post(request, *args, **kwargs)
    '''
    def form_valid(self, form) -> HttpResponse:
        self.create_object(form)

        payment_url = self.object.make_payment()
        if payment_url:
            return HttpResponseRedirect(redirect_to=payment_url)

        print("failed")
        return self.payment_create_faild()

    def create_object(self, form):
        self.object: AbstractPayment = form.save()
        self.object: AbstractPayment = AbstractPayment(
            comment='commentaire',
            mode='CIB',
            client='rania',
            client_email='rania@g.com',
            amount='2000',
        )
        self.object.save()


    def payment_create_faild(self):
        return HttpResponseRedirect(redirect_to=self.payment_create_faild_url)

    '''
class SponsorStatus(PaymentObjectDoneView):
    model = Sponsor
    template_name: str = "sponsor/sponsor-status.html"


class ConfirmSponsor(PaymentConfirmationView):
    model = Sponsor



