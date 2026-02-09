from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from .models import Ticket
import qrcode
import base64
from io import BytesIO

# --- GENERATOR SECTION ---
def generate_tickets(request):
    """
    Generates N tickets and displays them for printing/distribution.
    Run this BEFORE the event.
    """
    tickets_to_show = []
    
    if request.method == "POST":
        count = int(request.POST.get('count', 5))
        
        for _ in range(count):
            # Create DB entry
            new_ticket = Ticket.objects.create()
            
            # Generate QR Code Image
            qr = qrcode.QRCode(box_size=10, border=4)
            qr.add_data(new_ticket.ticket_id)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert image to base64 for HTML display
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            tickets_to_show.append({'id': new_ticket.ticket_id, 'qr_image': img_str})

    return render(request, 'generate.html', {'tickets': tickets_to_show})

def landing_page(request):
    """Renders the main dashboard."""
    return render(request, 'index.html')

# --- GATE SCANNER SECTION ---
def gate_scanner(request):
    """Renders the webcam scanning page."""
    return render(request, 'scanner.html')

def validate_ticket_api(request):
    """
    The AJAX endpoint called by the JS Scanner.
    This is where the One-Time Logic lives.
    """
    if request.method == "POST":
        scanned_code = request.POST.get('code')
        
        try:
            ticket = Ticket.objects.get(ticket_id=scanned_code)
            
            if ticket.is_used:
                return JsonResponse({
                    'status': 'error', 
                    'message': 'ALREADY USED!', 
                    'time': ticket.scanned_at
                })
            else:
                # MARK AS USED (The core state change)
                ticket.is_used = True
                ticket.scanned_at = timezone.now()
                ticket.save()
                return JsonResponse({'status': 'success', 'message': 'ENTRY GRANTED'})
                
        except Ticket.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'INVALID TICKET'})
            
    return JsonResponse({'status': 'error', 'message': 'Bad Request'})