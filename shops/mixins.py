from shops.models import Shop


class ClobberShopListModelMixin(object):
    def get_serializer(self, *args, **kwargs):
        """ if an array is passed, set serializer to many """
        if isinstance(kwargs.get('data', {}), list):
            Shop.objects.all().delete()
            kwargs['many'] = True
        return super(ClobberShopListModelMixin,
                     self).get_serializer(*args, **kwargs)
