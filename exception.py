from schemas.base_response  import BaseResponse

EXCEPTION_CODE = {
100001 : 'User not found!',
100002 : "Wrong password!",
100003 : 'Username already exist!',
100004 : 'Register Failed',
100005 : 'Update Password Failed',
100008:'Only for user',
100009:'Email does not exist!',
100010:'Only for admin!',
100011:'Email existed!',
100012: 'Password do not match'

}

def raise_error(error_code: int) -> BaseResponse:
    return BaseResponse(
        data = [],
        message=EXCEPTION_CODE.get(error_code),
        status='error',
    )
