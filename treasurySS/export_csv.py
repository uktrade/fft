def _export_sub_segment_iterator(queryset):
    yield [
        "Segment Grand Parent Code",
        "Segment Grand Parent Long Name",
        "Segment Parent Code",
        "Segment Parent Long Name",
        "Segment Code",
        "Segment Long Name",
        "Sub Segment Code",
        "Sub Segment Long Name",
        "Control budget detail code",
        "DBT Budget Code (used to generate the Oscar return)",
        "Accounting authority code",
        "Accounting authority detail code",
        "Estimates row code",
        "Estimates row long name",
        "Organisation",
        "Organisation Alias",
    ]
    for obj in queryset:
        yield [
            obj.Segment_code.segment_parent_code.segment_grand_parent_code.segment_grand_parent_code,  # noqa
            obj.Segment_code.segment_parent_code.segment_grand_parent_code.segment_grand_parent_long_name,  # noqa
            obj.Segment_code.segment_parent_code.segment_parent_code,
            obj.Segment_code.segment_parent_code.segment_parent_long_name,
            obj.Segment_code.segment_code,
            obj.Segment_code.segment_long_name,
            obj.sub_segment_code,
            obj.sub_segment_long_name,
            obj.control_budget_detail_code,
            obj.dit_budget_type.budget_type if obj.dit_budget_type else "-",
            obj.accounting_authority_code,
            obj.accounting_authority_DetailCode,
            obj.estimates_row_code.estimate_row_code,
            obj.estimates_row_code.estimate_row_long_name,
            obj.Segment_code.organization.organization_code,
            obj.Segment_code.organization.organization_alias,
        ]


def _export_segment_iterator(queryset):
    yield [
        "Segment Grand Parent Code",
        "Segment Grand Parent Long Name",
        "Segment Parent Code",
        "Segment Parent Long Name",
        "Segment Code",
        "Segment Long Name",
        "Organisation",
        "Organisation Alias",
    ]
    for obj in queryset:
        yield [
            obj.segment_parent_code.segment_grand_parent_code.segment_grand_parent_code,  # noqa
            obj.segment_parent_code.segment_grand_parent_code.segment_grand_parent_long_name,  # noqa
            obj.segment_parent_code.segment_parent_code,
            obj.segment_parent_code.segment_parent_long_name,
            obj.segment_code,
            obj.segment_long_name,
            obj.organization.organization_code,
            obj.organization.organization_alias,
        ]
