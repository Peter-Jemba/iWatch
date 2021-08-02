import json
import stripe
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from .models import Video

stripe.api_key = settings.STRIPE_SECRET_KEY

# VIDEOS_STRIPE_PRICING_ID = {
#     "video_basic": "price_1IvdrQCbPpOGhuNhxKH5XDBe",
#     "video_premium": "price_1IvdsRCbPpOGhuNhsH7qK79Q",
# }

class SuccessView(TemplateView):
    template_name = "success.html"

class CancelledView(TemplateView):
    template_name = "cancelled.html"
    

class VideoLandingPageView(TemplateView):
    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        video = Video.objects.get(title="War Room")
        context = super(VideoLandingPageView, self).get_context_data(**kwargs)
        context.update({
            "video":video,
            "STRIPE_PUBLISHABLE_KEY": settings.STRIPE_PUBLISHABLE_KEY
        })
        return context

    @csrf_exempt
    def stripe_config(request):
        if request.method == 'GET':
            stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
            return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_ENDPOINT_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)
        
        customer_email = session["customer_details"]["email"]
        video_id = session["metadata"]["video_id"]

        video = Video.objects.get(id=video_id)

        send_mail(
            subject="Here is your video",
            message=f"Thanks for your purchase. This is your . The URL is {video.url}",
            recipient_list=[customer_email],
            from_email="matt@test.com"
        )
    elif event["type"] == "payment_intent.succeeded":
        intent = event['data']['object']
        print[intent]

        stripe_customer_id = intent["customer"]
        stripe_customer = stripe.Customer.retrieve(stripe_customer_id)

        customer_email = stripe_customer['email']
        video_id = intent["metadata"]["video_id"]

        video = Video.objects.get(id=video_id)

        send_mail(
            subject="Here is your video",
            message=f"Thanks for your purchase. This is your . The URL is {video.url}",
            recipient_list=[customer_email],
            from_email="matt@test.com"
        )

    return HttpResponse(status=200)

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        video_id = self.kwargs["pk"]
        video = Video.objects.get(id=video_id)
        YOUR_DOMAIN = "http://127.0.0.0:8000/"
        print(video)
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        # 'price': VIDEOS_STRIPE_PRICING_ID[video_id],
                        'unit_amount': video.price,
                        'product_data': {
                            'name': video.title,
                            # 'images': ['https://i.imgur.com/EHyR2nP.png'],
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "video_id": video_id
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancelled/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })


class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            req_json=json.loads(request.body)
            customer = stripe.Customer.create(email=req_json['email'])
            video_id = self.kwargs["pk"]
            video = Video.objects.get(id=video_id)
            intent = stripe.PaymentIntent.create(
                amount= video.price,
                currency='usd',
                customer=customer['id'],
                metadata={
                    "video_id": video_id
                }
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({ "error": str(e) })
