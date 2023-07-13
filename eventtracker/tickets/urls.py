from django.urls import path, include

from tickets.views import AddToCartView, CartView, RemoveFromCartView, CreateCheckoutSessionView, SuccessView, \
    CancelledView, PurchasedTicketsView, download_ticket

urlpatterns = [
    path('event/<slug:slug>/add-to-cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/remove/<slug:slug>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('payments/', include('payments.urls')),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('cancel/', CancelledView.as_view(), name='cancelled'),
    path('success/', SuccessView.as_view(), name='success'),
    path('my-tickets/', PurchasedTicketsView.as_view(), name='purchased_tickets'),
    path('tickets/<int:ticket_id>/download/', download_ticket, name='download_ticket'),
]
