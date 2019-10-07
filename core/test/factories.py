from core.models import Document, EventLog, FinancialYear

import factory


class EventLogFactory(factory.DjangoModelFactory):
    """
    Define EventLog Factory
    """

    class Meta:
        model = EventLog


class FinancialYearFactory(factory.DjangoModelFactory):
    """
    Define FinancialYear Factory
    """

    class Meta:
        model = FinancialYear


class DocumentFactory(factory.DjangoModelFactory):
    """
    Define Document Factory
    """

    class Meta:
        model = Document
