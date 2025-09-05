Add substate (district) to states, sub-district (zone) to districts and cities to districts.
Changing state, dynamically reflect on districs. Smae thing for zones.

With this addons, Partner has disctics and zones.
You can integrate these features by just adding the mixin to your models.

class YourModel(models.AbstractModel):
    _name = 'your.model'
    _inherit = ['your.model', 'state.district.mixin']

Then add the following into your form view
<field name="city_id" placeholder="City" class="o_address_city"
        readonly="type == 'contact' and parent_id"
        context="{'state_id': state_id, 'default_state_id': state_id}"/>
<field name="district" placeholder="District" class="o_address_state"
        readonly="type == 'contact' and parent_id"
        context="{'state_id': state_id, 'default_state_id': state_id}"/>
<field name="zone" placeholder="Zone" class="o_address_zip"
        readonly="type == 'contact' and parent_id"
        context="{'district': district, 'default_district': district}"/>
