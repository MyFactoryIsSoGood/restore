from django.shortcuts import render
from .models import Gadget, Comment


# Create your views here.
def index(request, category=None):
    all_gadgets = Gadget.objects.all() if not category else Gadget.objects.filter(category=category)
    context = {
        'gadgets': [{'name': i.name, 'category': i.category, 'price': i.price, 'photo': i.photo, 'pk': i.pk} for i in
                    all_gadgets]}
    return render(request, 'main/index.html', context)


def item_page(request, pk):
    gadget = Gadget.objects.get(pk=pk)
    gadget_reviews = Comment.objects.filter(to_item=pk)
    reviews_count = len(gadget_reviews)
    average_rating = str(sum([i.rating for i in gadget_reviews]) / len(gadget_reviews))[:3] if gadget_reviews else 0
    context = {
        'gadget': {
            'name': gadget.name,
            'category': gadget.category,
            'price': gadget.price,
            'photo': gadget.photo,
            'reviews': [{'author': i.author_name,
                         'text': i.text,
                         'rating': i.rating,
                         'date': i.date_published
                         } for i in gadget_reviews]},
        'average_rating': average_rating,
        'based_on': 'Нет отзывов' if not gadget_reviews else (f'{reviews_count} отзыв' if reviews_count % 10 == 1 else (
            f'{reviews_count} отзыва' if reviews_count % 10 < 5 else f'{reviews_count} отзывов'))}
    return render(request, 'main/gadget_info.html', context)
