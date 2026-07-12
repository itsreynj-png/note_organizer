from .models import Course

def sidebar_courses(request):
    if request.user.is_authenticated:
        courses=Course.objects.filter(user=request.user)
    else:
        courses=[]

    return {"sidebar_course":courses}