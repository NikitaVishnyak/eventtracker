from datetime import timedelta

import stripe
from django.conf import settings
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from reportlab.graphics.shapes import Rect, Drawing

from eventsapp.models import Events
from tickets.models import Tickets, Cart
from django.shortcuts import redirect

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.units import inch
from io import BytesIO

from django.templatetags.static import static

stripe.api_key = settings.STRIPE_SECRET_KEY


class AddToCartView(View):
    def post(self, request, slug):
        event = get_object_or_404(Events, slug=slug)
        price = event.ticket_price * 100

        cart, created = Cart.objects.get_or_create(user=request.user)
        ticket = Tickets.objects.create(event=event, user=request.user, price=price)

        ticket.save()

        cart.tickets.add(ticket)

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

                # Add to the total cost
                total_price += ticket_price
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
                        'images': [ticket.event.image.url],
                    },
                },
                'quantity': 1,
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


def download_ticket(request, ticket_id):
    ticket = get_object_or_404(Tickets, id=ticket_id)
    event = ticket.event
    logo_path = finders.find('eventsapp/images/logo_new.png')
    event_image_path = event.image.path

    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0)

    styles = getSampleStyleSheet()
    header_style = styles['Heading1']
    header_style.backColor = colors.HexColor('#ff283e')

    title_style = ParagraphStyle(
        name="TitleStyle",
        parent=styles['Heading2'],
        fontSize=35,
        textColor=colors.black,
        spaceAfter=30,
        spaceBefore=6,
        bold=True,
    )

    info_style = ParagraphStyle(
        name="InfoStyle",
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.black,
        spaceAfter=6,
    )

    elements = []

    logo_image = Image(logo_path, width=6 * inch, height=0.48 * inch)

    logo_table = Table([[logo_image]], colWidths=[8.5 * inch], rowHeights=[1.5 * inch])

    logo_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#ff283e')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    elements.append(logo_table)

    event_image = Image(event_image_path, width=8.5 * inch, height=2.36 * inch)
    elements.append(event_image)

    elements.append(Spacer(1, 0.25 * inch))

    title_text = Paragraph(event.title, title_style)
    elements.append(title_text)

    elements.append(Paragraph(f"#{ticket.id}", info_style))
    elements.append(Paragraph(f"Full name: {ticket.user.get_full_name()}", info_style))
    elements.append(Paragraph(f"Start: {event.start_time}", info_style))
    elements.append(Paragraph(f"End: {event.end_time}", info_style))
    elements.append(Paragraph(f"Address: {event.address}, {event.city}", info_style))

    pdf.build(elements)

    buffer.seek(0)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{ticket.id}_{event.title}.pdf"'
    response.write(buffer.getvalue())

    return response
