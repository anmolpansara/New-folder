from rest_framework.exceptions import Throttled
from rest_framework.throttling import SimpleRateThrottle


class UserRateThrottle(SimpleRateThrottle):
    scope = "user"

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            return request.user.id
        return self.get_ident(request)

    def wait(self):
        """
        This method is called when the rate limit is exceeded.
        You can customize the error message here.
        """
        raise Throttled(
            detail="Your daily limit exceeded for this demo, please try again later."
        )
