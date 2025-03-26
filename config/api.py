from ninja import NinjaAPI


api = NinjaAPI()

api.add_router("/payroll/", "payroll.api.router")
