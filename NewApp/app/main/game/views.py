from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import json
import os
from datetime import datetime

def game(request):
    return render(request, 'game/game.html')

# @csrf_exempt
# def save_drawing(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
            
#             # Create drawings directory if it doesn't exist
#             drawings_dir = os.path.join(os.path.dirname(__file__), 'templates', 'game', 'drawings')
#             os.makedirs(drawings_dir, exist_ok=True)
            
#             # Generate unique filename using timestamp
#             timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#             filename = f'drawing_{timestamp}.json'
#             filepath = os.path.join(drawings_dir, filename)
            
#             # Save the drawing data
#             with open(filepath, 'w') as f:
#                 json.dump(data, f, indent=2)
            
#             return JsonResponse({'success': True, 'filename': filename})
            
#         except Exception as e:
#             return JsonResponse({'success': False, 'error': str(e)})
            
#     return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def waiting_room(request):
    username = request.session.get('username', None)
    return render(request, 'game/waiting_room.html', {'username': username})

def save_game_data(request):
    if request.method == 'POST':
        try:
            # Get the data from the POST request
            save_data = json.loads(request.body)
            # Save the data in the session (or database if needed)
            request.session['game_data'] = save_data

            # Return a success response
            return JsonResponse({'status': 'success', 'message': 'Game data saved successfully'})

        except Exception as e:
            # Handle errors and return a JSON response with error
            return JsonResponse({'status': 'error', 'message': str(e)})

    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

# Final results view
def final_results(request):
    score = request.GET.get('score')  # Get score from URL parameters
    game_data = request.session.get('game_data', [])
    
    # Now render the final results page with the data
    return render(request, 'game/final_results.html', {'score': score, 'game_data': game_data})
