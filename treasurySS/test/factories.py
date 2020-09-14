import factory

from chartofaccountDIT.models import BudgetType


from treasurySS.models import (
    EstimateRow,
    Segment,
    SegmentGrandParent,
    SegmentParent,
    SubSegment,
)


class SegmentGrandParentFactory(factory.DjangoModelFactory):
    """
    Define SegmentGrandParent Factory
    """

    class Meta:
        model = SegmentGrandParent
        django_get_or_create = ("segment_grand_parent_code",)


class SegmentParentFactory(factory.DjangoModelFactory):
    """
    Define SegmentParent Factory
    """

    segment_grand_parent_code = factory.SubFactory(SegmentGrandParentFactory)

    class Meta:
        model = SegmentParent
        django_get_or_create = ("segment_parent_code",)


class SegmentFactory(factory.DjangoModelFactory):
    """
    Define Segment Factory
    """

    segment_parent_code = factory.SubFactory(SegmentParentFactory)

    class Meta:
        model = Segment
        django_get_or_create = ("segment_code",)


class EstimateRowFactory(factory.DjangoModelFactory):
    """
    Define EstimateRow Factory
    """

    class Meta:
        model = EstimateRow


class SubSegmentFactory(factory.DjangoModelFactory):
    """
    Define SubSegment Factory
    """

    dit_budget_type = factory.Iterator(BudgetType.objects.all())

    Segment_code = factory.SubFactory(SegmentFactory)
    estimates_row_code = factory.SubFactory(EstimateRowFactory)

    class Meta:
        model = SubSegment
        django_get_or_create = ("sub_segment_code",)
