from core.utils.export_helpers import get_fk_value


def _export_gh_iterator(queryset):
    yield [
        "Original Record Id",
        "Record ID",
        "Category",
        "Gift or Hospitality",
        "Type",
        "Group",
        "Date Of Event / Gift Offered",
        "Venue",
        "Description Of Offer And Reason",
        "Estimated Value Of Offer (£)",
        "DIT Group Offered To/From",
        "DIT Representative Offered To/From",
        "Grade",
        "Offer",
        "Company Representative Offered To/From",
        "Company Offered To/From",
        # NB: Field - "Unspecified Company", may be required at a later date
        "Action Taken",
        "Date Entered",
        "Entered By",
    ]

    for obj in queryset:
        yield [
            obj.old_id,
            obj.id,
            get_fk_value(obj.category, "gif_hospitality_category"),
            get_fk_value(obj.classification, "gift_type"),
            get_fk_value(obj.classification, "gif_hospitality_classification"),
            obj.group_name,
            obj.date_agreed,
            obj.venue,
            obj.reason,
            obj.value,
            obj.rep,
            get_fk_value(obj.grade, "gradedescription"),
            obj.group,
            obj.get_offer_display(),
            obj.company_rep,
            obj.company,
            obj.company_name,
            obj.get_action_taken_display(),
            obj.entered_date_stamp,
            obj.entered_by,
        ]
