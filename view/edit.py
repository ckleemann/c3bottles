from datetime import datetime
from flask import render_template, request, g, abort
from flask.ext.login import login_required

from controller import c3bottles, db
from model.drop_point import DropPoint
from model.location import Location
from model.capacity import Capacity

@c3bottles.route("/edit/<string:number>", methods=("GET", "POST"))
@c3bottles.route("/edit")
@login_required
def edit_dp(
        number=None, description=None, lat=None,
        lng=None, level=None, crates=None, errors=None,
        success=None, center_lat=None, center_lng=None
):

    if not g.user.can_edit:
        abort(401)

    if number:
        dp = DropPoint.get(number)
    else:
        dp = DropPoint.get(request.values.get("number"))

    if not dp:
        return render_template(
            "error.html",
            heading="Error!",
            text="Drop point not found."
        )

    description_old = str(dp.get_current_location().description)
    lat_old = str(dp.get_current_location().lat)
    lng_old = str(dp.get_current_location().lng)
    level_old = str(dp.get_current_location().level)
    crates_old = str(dp.get_current_crate_count())

    if request.method == "POST":

        description = request.form.get("description")
        lat = request.form.get("lat")
        lng = request.form.get("lng")
        level = request.form.get("level")
        crates = request.form.get("crates")
        remove = request.form.get("remove")

        try:

            if description != description_old \
                    or lat != lat_old or lng != lng_old:
                Location(
                    dp,
                    description=description,
                    lat=lat,
                    lng=lng,
                    level=level
                )

            if crates != crates_old:
                Capacity(
                    dp,
                    crates=crates
                )

            if remove == "yes":
                dp.removed = datetime.now()

        except ValueError as e:
            errors = e.args
        else:
            db.session.commit()
            return render_template(
                    "success.html",
                    text="Your changes have been saved."
                )

    else:
        description = description_old
        lat = lat_old
        lng = lng_old
        level = level_old
        crates = crates_old

    try:
        lat_f = float(lat)
        lng_f = float(lng)
    except (ValueError, TypeError):
        lat_f = None
        lng_f = None

    if errors is not None:
        error_list = [v for d in errors for v in d.values()]
        error_fields = [k for d in errors for k in d.keys()]
    else:
        error_list = []
        error_fields = []

    return render_template(
        "edit_dp.html",
        all_dps_json=DropPoint.get_dps_json(),
        number=number,
        description=description,
        lat=lat_f,
        lng=lng_f,
        level=level,
        crates=crates,
        error_list=error_list,
        error_fields=error_fields
    )

# vim: set expandtab ts=4 sw=4:
