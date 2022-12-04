from site_app.models import SiteSetting, InstagramImage, DiscountAd


def site_setting(request):
    return {
        "site_setting": SiteSetting.objects.filter(is_main_setting=True).first()
    }


def instagram_images(request):
    return {
        "instagram_images": InstagramImage.objects.filter(is_active=True)
    }


def discount_ads(request):
    return {
        "discount_ads": DiscountAd.objects.filter(is_active=True)
    }
