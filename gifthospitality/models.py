# from django.db import models
#
# from core.metamodels import TimeStampedModel
#
# from costcentre.models import DepartmentalGroup
#
# from payroll.models import Grade


# Gift and Hospitality
# class GiftsAndHospitality(TimeStampedModel):
#     classification = models.CharField(max_length=50)
#     type = models.CharField(max_length=50)
#     # group_code = models.ForeignKey(DepartmentalGroup, on_delete=models.PROTECT)
#     date_offered = models.DateTimeField()
#     venue = models.CharField(max_length=1000)
#     reason = models.CharField(max_length=1000)
#     value = models.DecimalField(max_digits=18, decimal_places=2)
#     band = models.CharField(max_length=50)
#     rep = models.CharField(max_length=255)
#     offer = models.CharField(max_length=50)
#     company_rep = models.CharField(max_length=50)
#     company = models.CharField(max_length=255)
#     action_taken = models.CharField(max_length=50)
#     date_stamp = models.DateTimeField()
#     entered_by = models.CharField(max_length=50)
#     staff_no = models.CharField(max_length=50)
#     entered_date_stamp = models.DateTimeField()
#     category = models.CharField(max_length=255)
#     grade = models.ForeignKey(Grade, on_delete=models.PROTECT)

# class HotelAndTravel(TimeStampedModel):
#     traveller_name = models.CharField(max_length=500)
#     product_type = models.CharField(max_length=500)
#     room_nights = models.IntegerField()
#     travel_date = models.CharField(max_length=10)
#     routing = models.CharField(max_length=500)
#     geog_indicator = models.CharField(max_length=500)
#     hotel_city = models.CharField(max_length=500)
#     class_of_service = models.CharField(max_length=500)
#     rail_journey_type = models.CharField(max_length=500)
#     hotel_name = models.CharField(max_length=500)
#     supplier_name = models.CharField(max_length=500)
#     fee_paid = models.DecimalField(max_digits=18, decimal_places=2)
#     int_dom = models.CharField(max_length=500)
#     reason_code_desc = models.CharField(max_length=500)
#     cost_centre = models.ForeignKey(CostCentre, on_delete=models.PROTECT)
#     programme = models.ForeignKey(ProgrammeCode, on_delete=models.PROTECT)
#     natural_account_code = models.ForeignKey(NaturalCode, on_delete=models.PROTECT)
