from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic.edit import CreateView

from .models import Gadget, Comment
from .forms import CommentForm


class CommentAddView(CreateView):
    template_name = 'main/gadget_info.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_id = int(self.kwargs.get('pk'))
        gadget = Gadget.objects.get(pk=item_id)
        reviews_all = Comment.objects.filter(to_item=item_id)
        reviews_count = len(reviews_all)
        ratings = [
            (len(reviews_all.filter(rating=i)), int(len(reviews_all.filter(rating=i)) / (reviews_count + 0.1) * 100))
            for i
            in range(1, 6)]
        gadget = {
            'name': gadget.name,
            'category': gadget.category,
            'price': gadget.price,
            'photo': gadget.photo,
            'reviews': [{'author': i.author_name,
                         'text': i.text,
                         'rating': i.rating,
                         'date': i.date_published
                         } for i in reviews_all]
        }
        reviews = {
            'count': reviews_count,
            'r1': {'count': ratings[0][0],
                   'percentage': ratings[0][1] if ratings[0][1] != 0 else 2},
            'r2': {'count': ratings[1][0],
                   'percentage': ratings[1][1] if ratings[1][1] != 0 else 2},
            'r3': {'count': ratings[2][0],
                   'percentage': ratings[2][1] if ratings[2][1] != 0 else 2},
            'r4': {'count': ratings[3][0],
                   'percentage': ratings[3][1] if ratings[3][1] != 0 else 2},
            'r5': {'count': ratings[4][0],
                   'percentage': ratings[4][1] if ratings[4][1] != 0 else 2}
        }
        average_rating = str(sum([i.rating for i in reviews_all]) / len(reviews_all))[:3] if reviews_all else 0
        context['gadget'] = gadget
        context['average_rating'] = average_rating
        context['based_on'] = 'Нет отзывов' if not reviews_all else (
            f'{reviews_count} отзыв' if reviews_count % 10 == 1 else (
                f'{reviews_count} отзыва' if reviews_count % 10 < 5 else f'{reviews_count} отзывов'))
        context['reviews'] = reviews
        return context

    def get_success_url(self):
        item_id = int(self.kwargs.get('pk'))
        success_url = f'/gadget_{item_id}/'
        return success_url

    def form_valid(self, form):
        item_id = int(self.kwargs.get('pk'))
        gadget = Gadget.objects.get(pk=item_id)
        form.instance.to_item = gadget
        return super(CommentAddView, self).form_valid(form)


def index(request, category=None):
    all_gadgets = Gadget.objects.all() if not category else Gadget.objects.filter(category=category)
    if request.GET.get('q'):
        query = request.GET.get('q')
        all_gadgets = all_gadgets.filter(name__icontains=query)
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
    print(context)
    return render(request, 'main/gadget_info.html', context)
