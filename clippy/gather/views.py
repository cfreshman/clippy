from django.shortcuts import render

# Create your views here.
def index(request):
    """
    View function for home page of site.
    """
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'group_list': [{'id': str(i+1)} for i in range(4)], 'group_id': 0,
        		 'event_list': range(3), 
        		 'slide_title': 'Going','slide_list': range(2)},
    )

def user(request, id):
    return render(
        request,
        'user.html',
        context={'group_list': [{'id': str(i+1)} for i in range(4)], 'group_id': -1, 
        		 'event_list': range(1), 
        		 'slide_title': 'Your Groups', 'slide_list': range(1)},
    )

def group(request, id):
    return render(
        request,
        'group.html',
        context={'group_list': [{'id': str(i+1)} for i in range(4)],'group_id': id,
        		 'event_list': range(2), 
        		 'slide_title': 'Members', 'slide_list': range(4)},
    )