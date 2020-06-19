from django.core.mail import send_mail
from rest_framework import serializers

from safe_internet_app.models import Inquiry


class InquirySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    url = serializers.URLField(allow_blank=False)
    reason = serializers.CharField(allow_blank=True)
    email = serializers.EmailField(allow_blank=False)


    def create(self, validated_data):
        x_forwarded_for = self.context['request'].META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.context['request'].META.get('REMOTE_ADDR')

        validated_data['issuer_ip'] = ip
        validated_data['open_for_review'] = True

        return Inquiry.objects.create(**validated_data)


    def update(self, instance, validated_data):

        ban_website = self.context['request'].data['block']

        if ban_website:
            instance.open_for_review = False
            instance.website_blocked = True
        else:
            instance.open_for_review = False

        send_mail(
            'Hello there.',
            'Roskomnadzor reviewed your inquiry.',
            'roskompozor@mail.ru',
            [f'{instance.email}'],
        )

        instance.save()
        return instance
