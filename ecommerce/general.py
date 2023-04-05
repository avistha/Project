
from . models import Category, Settings

def global_data(request):
    data = {
        'categoryData' : Category.objects.all(),
        'settingData' : Settings.objects.last(),
    }
    return data
