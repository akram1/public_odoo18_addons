Replace categories, tags, states, types and stages with one common manageable tag app.

This module allows you to create and categorize tags (keywords).
With these tags in other applications, you can use the logic associated with
them (for example, search and filter objects by tags). All Tags are manageable
in Tag app, therefore, define tags in your application and manage and expand
tag definitions in one place.
You have 4 types of tags:
    - Tag: this can be multi or single choice. Ex, categories for products.
            Tags are categories per model. For example, your can categories
            customer person (partner) sex, eye color, religion, ethnicity,
            medical_aid, blood_group. Once you select multi choice Tag,
            you can select multiple tags for a record.
    - Type: this can be single choice. Ex, type of product.
    - State: this can be single choice. Ex, state of process.
    - Reason: this can be single choice. Ex, reason of disapprove or state.
You can set which tag is required and the default value. To integrate these
tags in your module, use simple mixin.

class YourModel(models.Model):
    _name = "your.model"
    _inherit = ["tag.mixin"]

For Tag, use tag.mixin. For Type, use tag.type.mixin. For State, Reason and Type
use tag.state.mixin.

To add tags to views:
For search view
        <field name="fld_tags"
            options="{'color_field': 'color'}"/>
        <field name="search_tags"/>
        <field name="search_no_tags"/>

List view
            <field name="fld_tags"
                options="{'color_field': 'color', 'no_create': True}"
                context="{'search_default_group_by_category': 1}"
                widget="many2many_tags"
                placeholder="Tags..."/>
Form view
            <field name="fld_tags"
                options="{'color_field': 'color', 'no_create': True}"
                context="{'search_default_group_by_category': 1,
                            'default_model_name': 'account.move'}"
                widget="many2many_tags"
                placeholder="Tags..."/>

There is a separate module for state called tag_state. This extends state to
new level of features such as state workflow and process. Check Tag State
module for details.
Also there are free addons to integrate Tag into partner, employee, product and accounting.
