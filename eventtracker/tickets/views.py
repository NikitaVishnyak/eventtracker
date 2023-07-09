from datetime import timedelta

import stripe
from django.conf import settings
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView

from eventsapp.models import Events
from tickets.models import Tickets, Cart
from django.shortcuts import redirect

stripe.api_key = settings.STRIPE_SECRET_KEY


class AddToCartView(View):
    def get(self, request, slug):
        event = get_object_or_404(Events, slug=slug)
        return render(request, 'add_to_cart.html', {'event': event})

    def post(self, request, slug):
        event = get_object_or_404(Events, slug=slug)
        ticket_quantity = int(request.POST.get('ticket_quantity', 0))
        price = event.ticket_price * 100

        if ticket_quantity > 0:
            cart, created = Cart.objects.get_or_create(user=request.user)
            tickets = Tickets.objects.create(event=event, user=request.user, price=price)

            tickets.quantity += ticket_quantity
            tickets.save()

            cart.tickets.add(tickets)

        return redirect('cart')


class CartView(View):
    def get(self, request):
        cart = Cart.objects.get(user=request.user)
        tickets = cart.tickets.all()

        total_price = 0
        expiration_time = None

        for ticket in tickets:
            expiration_time = ticket.created_at + timedelta(minutes=20)
            # Check and delete reserved tickets
            if timezone.now() > expiration_time:
                cart.tickets.remove(ticket)
                ticket.delete()

            try:
                # Calculate the cost of a ticket
                ticket_price = ticket.event.ticket_price
                quantity = ticket.quantity
                ticket_total_price = ticket_price * quantity

                # Add to the total cost
                total_price += ticket_total_price
            except UnboundLocalError:
                total_price = 0

        # Save changes
        cart.save()

        timestamp = request.session.get('cart_timestamp')  # Get update time from the session
        if not timestamp:
            timestamp = timezone.now()
            request.session['cart_timestamp'] = str(timestamp)  # Save update time in the session

        if expiration_time is not None:
            expiration_time_str = expiration_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        else:
            expiration_time_str = None

        context = {
            'cart': cart,
            'tickets': tickets,
            'timestamp': timestamp,
            'expiration_time': expiration_time_str,
            'total_price': total_price,
        }

        return render(request, 'cart.html', context)


class RemoveFromCartView(View):
    def post(self, request, slug):
        event = get_object_or_404(Events, slug=slug)
        tickets = Tickets.objects.filter(event=event.id, user=request.user, is_paid=False)
        print(tickets)
        cart = Cart.objects.get(user=request.user)
        for ticket in tickets:
            cart.tickets.remove(ticket)
            ticket.delete()

        return redirect('cart')


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        DOMAIN = "http://127.0.0.1:8000"
        tickets = Tickets.objects.filter(user=request.user, is_paid=False)

        line_items = []
        for ticket in tickets:
            line_items.append({
                'price_data': {
                    'currency': 'EUR',
                    'unit_amount': int(ticket.event.ticket_price * 100),
                    'product_data': {
                        'name': ticket.event.title,
                        'images': [DOMAIN + ticket.event.image.url],
                    },
                },
                'quantity': ticket.quantity,
            })

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=DOMAIN + '/success/',
            cancel_url=DOMAIN + '/cancel/',
        )
        return redirect(checkout_session.url, code=303)


class SuccessView(View):
    def get(self, request):
        cart = Cart.objects.get(user=request.user)
        tickets = cart.tickets.filter(is_paid=False)
        for ticket in tickets:
            ticket.is_paid = True
            ticket.save()
            cart.tickets.remove(ticket)
        cart.tickets.clear()
        cart.save()
        return render(request, 'success_payment.html')


class CancelledView(TemplateView):
    template_name = "cancelled_payment.html"


class PurchasedTicketsView(View):
    def get(self, request):
        tickets = Tickets.objects.filter(user=request.user, is_paid=True)
        context = {
            'tickets': tickets,
        }
        return render(request, 'purchased_tickets.html', context)
