from django.http import JsonResponse
import re


class ApiOrder():

    @classmethod
    def validate_order(cls, order_dict, fields):
        errors = []
        fields_dict = {}
        for field in fields:
            if field.name not in order_dict and field.is_required:
                errors.append(cls._no_field_error(field.name))
            else:
                print("OD", order_dict)
                try: field_val = order_dict[str(field.pk)]
                except KeyError: continue
                 
                pattern = re.compile(field.pattern)
                if pattern.match(str(field_val)):
                    fields_dict[str(field.pk)] = field_val
                else:
                    errors.append(field.error_msg)
        return (fields_dict, errors)

    @staticmethod
    def _no_field_error(fname):
        return "Required field `{0}` not passed.".format(fname)



class ErrCodes():
    format_err = 1
    arg_err = 2
    token_err = 3
    invite_err = 4
    fields_not_created_err = 5
    invalid_form_err = 6
    internal_err = 7


class ApiResponse():
    @staticmethod
    def success():
        return JsonResponse({"is_success": True}, safe=False)

    @staticmethod
    def success_result(result={}):
        return JsonResponse({"is_success": True, "result":result}, safe=False)


    @staticmethod
    def failure(cause, err_code=1):
        return JsonResponse({
            "is_success": False,
            "error_code": err_code,
            "cause": cause,
        }, safe=False)

    @staticmethod
    def failure_form_not_valid(form_errors, cause="Order form does't match the fromat."):
        return JsonResponse({
            "is_success": False,
            "error_code": ErrCodes.invalid_form_err,
            "cause": cause,
            "form_errors": form_errors,
        }, safe=False)
