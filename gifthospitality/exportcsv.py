from core.exportutils import get_fk_value


def _export_gh_iterator(queryset):
    yield ['Original Record Id', 'Record ID',
           'Category',
           'Gift or Hospitality', 'Type', 'Group',
            'Date Of Event / Gift Offered', 'Venue',
            'Description Of Offer And Reason',
            'Estimated Value Of Offer (£)',
            'DIT Representative Offered To/From',
            'Grade', 'Offer',
            'Company Representative Offered To/From',
            'Company Offered To/From',
            'Action Taken',
            'Date Entered',
            'Entered By']

    for obj in queryset:
        yield [obj.old_id,
               obj.id,
               get_fk_value(obj.category_fk,'gif_hospitality_category'),
               get_fk_value(obj.classification_fk,'gift_type'),
               get_fk_value(obj.classification_fk,'gif_hospitality_classification'),
               obj.group_name,
               obj.date_offered,
               obj.venue,
               obj.reason,
               obj.value,
               obj.rep,
               get_fk_value(obj.grade_fk,'gradedescription'),
               obj.get_offer_display(),
               obj.company_rep,
               obj.company,
               obj.get_action_taken_display(),
               obj.entered_date_stamp,
               obj.entered_by]


