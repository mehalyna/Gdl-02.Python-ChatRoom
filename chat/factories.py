import factory

from . import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    username = factory.Faker("user_name")
    password = factory.Faker("password")
    email = factory.Sequence(lambda n: "person{}@example.com".format(n))
    role = factory.Iterator(models.Role.objects.all())


class ChatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Chat

    chat_name = factory.Faker("domain_word")
    description = factory.Faker("sentence", nb_words=20)
    created_at = factory.Faker("date_this_year")

    # chat_member - manytomany field
    # from existing data passed as param while creating assigns member
    @factory.post_generation
    def chat_member(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for member in extracted:
                self.chat_member.add(member)

    # moderator - manytomany field
    # from existing data passed as param while creating assigns moderator
    @factory.post_generation
    def moderator(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for chat_user in extracted:
                self.moderator.add(chat_user)


class MessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Message

    content = factory.Faker("sentence", nb_words=30)
    created_at = factory.Faker("date_this_year")
    chat = factory.Iterator(models.Chat.objects.all())
    # from existing chat_members of the chat, mix and select first to keep consistency
    user = factory.LazyAttribute(
        lambda obj: models.Chat.objects.get(pk=obj.chat.pk)
        .chat_member.all()
        .order_by("?")
        .first()
    )
