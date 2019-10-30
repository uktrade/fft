import factory

from downloadsupport.models import DownloadLog


class DownloadLogFactory(factory.DjangoModelFactory):
    """
    Define DownloadLog Factory
    """

    class Meta:
        model = DownloadLog
