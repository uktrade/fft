from downloadsupport.models import DownloadLog

import factory


class DownloadLogFactory(factory.DjangoModelFactory):
    """
    Define DownloadLog Factory
    """

    class Meta:
        model = DownloadLog
