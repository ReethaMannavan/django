from rest_framework.throttling import UserRateThrottle

class PostBlogThrottle(UserRateThrottle):
    scope = 'post_blog'
