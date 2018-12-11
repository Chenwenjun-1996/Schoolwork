import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from ForceMap import ForceMap


# Create your views here.

@csrf_exempt
def display(request):
    if request.method == 'POST':
        data = request.POST
        #        print(type(json.loads(data.get('graph'))))

        force = ForceMap(json.loads(data.get('graph')), int(data.get('width')), int(data.get('height')),
                         int(data.get('dx')),
                         int(data.get('dy')), int(data.get('people')))
        info = {}
        info['ori'] = force.personMap()
        #print(force.personMap())
        info['st'] = []
        for i in range(120):
            force.step()
            #print(force.personMap())
            info['st'].append(force.personMap())
        return JsonResponse(info)
    else:
        return JsonResponse({})


def drawMap(request):
    return render(request, 'map.html')
