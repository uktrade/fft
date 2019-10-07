from treasurySS.models import EstimateRow, Segment, SegmentGrandParent, SegmentParent, SubSegment

import factory


class SegmentGrandParentFactory(factory.DjangoModelFactory):
    """
    Define SegmentGrandParent Factory
    """

    class Meta:
        model = SegmentGrandParent


class SegmentParentFactory(factory.DjangoModelFactory):
    """
    Define SegmentParent Factory
    """

    class Meta:
        model = SegmentParent


class SegmentFactory(factory.DjangoModelFactory):
    """
    Define Segment Factory
    """

    class Meta:
        model = Segment


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

    class Meta:
        model = SubSegment
