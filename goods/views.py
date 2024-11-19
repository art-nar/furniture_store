from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.contrib import messages
from goods.models import Categories, Products
from goods.utils import q_search


class CatalogView(ListView):
    model = Products
    # queryset = Products.objects.all().order_by("-id")
    template_name = "goods/catalog.html"
    context_object_name = "goods"
    paginate_by = 3
    allow_empty = False

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            messages.warning(self.request, "В этой категории нет товаров. Выберите другую категорию, пожалуйста.")

            return HttpResponseRedirect(reverse("main:index"))

    def get_queryset(self):
        category_slug = self.kwargs.get("category_slug")
        on_sale = self.request.GET.get("on_sale", None)
        order_by = self.request.GET.get("order_by", None)
        query = self.request.GET.get("q", None)

        if category_slug == "vse-tovary":
            goods = super().get_queryset()
        elif query:
            goods = q_search(query)
        else:
            goods = super().get_queryset().filter(category__slug=category_slug)
            if not goods.exists():
                raise Http404()

        if on_sale:
            goods = goods.filter(discount__gt=0)

        if order_by and order_by != "default":
            goods = goods.order_by(order_by)

        return goods

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - Каталог"
        context["slug_url"] = self.kwargs.get("category_slug")
        context["categories"] = Categories.objects.all()
        return context


class ProductView(DetailView):

    # model = Products
    # slug_field = "slug"
    template_name = "goods/product.html"
    slug_url_kwarg = "product_slug"
    context_object_name = "product"

    def get_object(self, queryset=None):
        product = Products.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.name
        return context


# def catalog(request, category_slug=None):
#     page = request.GET.get("page", 1)
#     on_sale = request.GET.get("on_sale", None)
#     order_by = request.GET.get("order_by", None)
#     query = request.GET.get("q", None)

#     if category_slug == "vse-tovary":
#         goods = Products.objects.all()
#     elif query:
#         goods = q_search(query)
#     else:
#         goods = Products.objects.filter(category__slug=category_slug)
#         if not goods.exists():
#             raise Http404()

#     if on_sale:
#         goods = goods.filter(discount__gt=0)

#     if order_by and order_by != "default":
#         goods = goods.order_by(order_by)

#     paginator = Paginator(goods, 3)
#     current_page = paginator.page(int(page))

#     context = {
#         "title": "Home - Каталог",
#         "goods": current_page,
#         "slug_url": category_slug,
#     }
#     return render(request, "goods/catalog.html", context)


# def product(request, product_slug):

#     products = Products.objects.get(slug=product_slug)

#     context = {"product": products}
#     return render(request, "goods/product.html", context)
