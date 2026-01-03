from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .solitaire import SolitaireGame


def index(request):
    """Render the main game page."""
    return render(request, 'game/index.html')


def new_game(request):
    """Start a new game and save to session."""
    game = SolitaireGame()
    request.session['game_state'] = game.to_json()
    return JsonResponse(game.get_state())


def get_game_state(request):
    """Get current game state from session."""
    game_json = request.session.get('game_state')
    if not game_json:
        game = SolitaireGame()
        request.session['game_state'] = game.to_json()
    else:
        game = SolitaireGame.from_json(game_json)
    
    return JsonResponse(game.get_state())


def draw_card(request):
    """Draw a card from the deck."""
    game_json = request.session.get('game_state')
    if not game_json:
        return JsonResponse({'error': 'No game in progress'}, status=400)
    
    game = SolitaireGame.from_json(game_json)
    game.draw_card()
    request.session['game_state'] = game.to_json()
    
    return JsonResponse(game.get_state())


@csrf_exempt
def move_card(request):
    """Move a card from one location to another."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    game_json = request.session.get('game_state')
    if not game_json:
        return JsonResponse({'error': 'No game in progress'}, status=400)
    
    try:
        data = json.loads(request.body)
        from_loc = data.get('from')
        to_loc = data.get('to')
        card_index = data.get('card_index')
        
        game = SolitaireGame.from_json(game_json)
        success = game.move_card(from_loc, to_loc, card_index)
        
        if success:
            request.session['game_state'] = game.to_json()
            return JsonResponse({'success': True, 'state': game.get_state()})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid move'})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def auto_move(request):
    """Automatically move cards to foundations."""
    game_json = request.session.get('game_state')
    if not game_json:
        return JsonResponse({'error': 'No game in progress'}, status=400)
    
    game = SolitaireGame.from_json(game_json)
    moved = game.auto_move_to_foundation()
    request.session['game_state'] = game.to_json()
    
    return JsonResponse({'moved': moved, 'state': game.get_state()})