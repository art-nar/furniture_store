from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="category name")
    slug = models.SlugField(
        max_length=200, unique=True, blank=True, null=True, verbose_name="URL"
    )

    class Meta:
        db_table = "category"
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="product name")
    slug = models.SlugField(
        max_length=200, unique=True, blank=True, null=True, verbose_name="URL"
    )
    description = models.TextField(
        blank=True, null=True, verbose_name="product description"
    )
    image = models.ImageField(
        upload_to="goods_images", blank=True, null=True, verbose_name="image"
    )
    price = models.DecimalField(
        default=0.00, max_digits=7, decimal_places=2, verbose_name="price"
    )
    discount = models.DecimalField(
        default=0.00, max_digits=4, decimal_places=2, verbose_name="discount in %"
    )
    quantity = models.PositiveIntegerField(default=0, verbose_name="quantity")
    category = models.ForeignKey(
        to=Categories, on_delete=models.CASCADE, verbose_name="category"
    )

    class Meta:
        db_table = "product"
        verbose_name = "product"
        verbose_name_plural = "products"

    def __str__(self):
        return self.name

    def display_id(self):
        return f"{self.id:05}"

    def self_price(self):
        if self.discount:
            return round(self.price - (self.price * self.discount) / 100, 2)
        return self.price
