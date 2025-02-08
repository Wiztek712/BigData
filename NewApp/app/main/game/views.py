from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
import os
from datetime import datetime

def game(request):
    return render(request, 'game/game.html')

@csrf_exempt
def save_drawing(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Create drawings directory if it doesn't exist
            drawings_dir = os.path.join(os.path.dirname(__file__), 'templates', 'game', 'drawings')
            os.makedirs(drawings_dir, exist_ok=True)
            
            # Generate unique filename using timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'drawing_{timestamp}.json'
            filepath = os.path.join(drawings_dir, filename)
            
            # Save the drawing data
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            
            return JsonResponse({'success': True, 'filename': filename})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
            
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def waiting_room(request):
    return render(request, 'game/waiting_room.html')

def final_results(request):
    return render(request, 'game/final_results.html')
