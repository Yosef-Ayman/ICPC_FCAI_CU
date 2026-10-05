from django.http import JsonResponse


def success_response(data=None, message="", status=200):
    return JsonResponse(
        {
            "success": True,
            "data": data,
            "message": message,
        },
        status=status,
    )


def error_response(message, data=None, status=400):
    return JsonResponse(
        {
            "success": False,
            "data": data,
            "message": message,
        },
        status=status,
    )