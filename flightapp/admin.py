from flightapp import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flightapp.models import ChuyenbayMotChang, ChuyenBayNhieuChang, TuyenBay

admin = Admin(app=app, name='Quản trị máy bay', template_mode='bootstrap4')


class ChuyenBay1ChangView(ModelView):
    can_view_details = True


class ChuyenBayNhieuChangView(ModelView):
    can_view_details = True


class TuyenBayView(ModelView):
    can_view_details = True


admin.add_view(ChuyenBay1ChangView(ChuyenbayMotChang, db.session))
admin.add_view(ChuyenBayNhieuChangView(ChuyenBayNhieuChang, db.session))
admin.add_view(TuyenBayView(TuyenBay, db.session))
