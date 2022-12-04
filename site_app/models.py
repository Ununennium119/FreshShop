import uuid

from django.db import models


class SiteSetting(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    site_name = models.CharField(max_length=64)
    site_url = models.URLField(max_length=256)

    address = models.CharField(max_length=256, null=True, blank=True)
    phone = models.CharField(max_length=16, null=True, blank=True)
    email = models.CharField(max_length=256, null=True, blank=True)
    facebook_link = models.URLField(max_length=256, null=True, blank=True)
    twitter_link = models.URLField(max_length=256, null=True, blank=True)
    youtube_link = models.URLField(max_length=256, null=True, blank=True)
    instagram_link = models.URLField(max_length=256, null=True, blank=True)
    pinterest_link = models.URLField(max_length=256, null=True, blank=True)

    about_us_text = models.TextField(null=True, blank=True)
    contact_us_text = models.TextField(null=True, blank=True)
    copy_right_text = models.TextField(null=True, blank=True)
    site_logo = models.ImageField(upload_to="site-setting")

    is_main_setting = models.BooleanField(default=False)

    def __str__(self):
        return str(self.site_name)


class BusinessTime(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    site_setting = models.ForeignKey(SiteSetting, on_delete=models.CASCADE, related_name="business_times_set")
    text = models.CharField(max_length=64)


class TeamMember(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=128)
    position = models.CharField(max_length=128)
    short_introduction = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="member-images")

    facebook_link = models.URLField(max_length=256, null=True, blank=True)
    twitter_link = models.URLField(max_length=256, null=True, blank=True)
    youtube_link = models.URLField(max_length=256, null=True, blank=True)
    linkedin_link = models.URLField(max_length=256, null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)


class SliderImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    image = models.ImageField(upload_to="sliders")
    is_active = models.BooleanField(default=True)


class InstagramImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    image = models.ImageField(upload_to="instagram")
    is_active = models.BooleanField(default=True)


class ContactInfo(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=128)
    email = models.EmailField(max_length=256)
    subject = models.CharField(max_length=128)
    message = models.TextField()
    is_responded = models.BooleanField(default=False)


class DiscountAd(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    text = models.CharField(max_length=128)
    is_active = models.BooleanField()
