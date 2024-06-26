from ..models import TagModel, LinkTagAndClientModel
from ..exceptions import BadRequest


def create_link_tags(client_instance, tags):
    '''Создание связи между клиентом и тэгом'''
    tags = set(tags)

    tag_instances = TagModel.objects.filter(pk__in=tags).all()

    if len(tags) != len(tag_instances):
        raise BadRequest()

    links = LinkTagAndClientModel.objects.bulk_create(
        [LinkTagAndClientModel(client=client_instance, tag=tag_instance) for tag_instance in tag_instances]
    )

    return list(links)
