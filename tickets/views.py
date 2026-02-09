from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from .models import Ticket
import qrcode
import base64
from io import BytesIO
import zipfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def generate_ticket_image(ticket_id, design_config=None):
    """
    Generate a classy LANDSCAPE ticket image with custom design using Pillow.
    Returns base64 encoded image and PIL Image object.
    """
    # Default design if none provided
    if not design_config:
        design_config = {
            'event_name': 'EVENT PASS',
            'ticket_type': 'entry',
            'price': 0,
            'primary_color': '#2563eb',
            'secondary_color': '#1e40af',
            'background_style': 'gradient'
        }
    
    # Ticket dimensions - LANDSCAPE (wider than tall)
    width, height = 800, 350
    
    # Create base image with colored background
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # Parse colors
    primary_rgb = hex_to_rgb(design_config['primary_color'])
    secondary_rgb = hex_to_rgb(design_config['secondary_color'])
    
    # Create full background gradient
    if design_config['background_style'] == 'gradient':
        for x in range(width):
            ratio = x / width
            r = int(primary_rgb[0] * (1 - ratio) + secondary_rgb[0] * ratio)
            g = int(primary_rgb[1] * (1 - ratio) + secondary_rgb[1] * ratio)
            b = int(primary_rgb[2] * (1 - ratio) + secondary_rgb[2] * ratio)
            draw.rectangle([(x, 0), (x + 1, height)], fill=(r, g, b))
    else:
        draw.rectangle([(0, 0), (width, height)], fill=primary_rgb)
    
    # Add subtle decorative circles pattern (very light)
    for i in range(0, width, 100):
        for j in range(0, height, 100):
            # Draw semi-transparent circles
            overlay = Image.new('RGBA', (width, height), (255, 255, 255, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            overlay_draw.ellipse([(i-25, j-25), (i+25, j+25)], fill=(255, 255, 255, 15))
            img.paste(overlay, (0, 0), overlay)
    
    # Add very subtle diagonal accent lines (minimal)
    overlay = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    for i in range(-height, width, 120):
        overlay_draw.line([(i, 0), (i + height, height)], fill=(255, 255, 255, 8), width=2)
    img.paste(overlay, (0, 0), overlay)
    
    # Try to load fonts
    try:
        title_font = ImageFont.truetype("arial.ttf", 48)
        subtitle_font = ImageFont.truetype("arial.ttf", 28)
        info_font = ImageFont.truetype("arial.ttf", 20)
        small_font = ImageFont.truetype("arial.ttf", 14)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        info_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # LEFT SECTION - Event Information
    left_margin = 40
    
    # Event name (top left)
    event_name = design_config['event_name']
    draw.text((left_margin, 50), event_name.upper(), 
              fill='white', font=title_font)
    
    # Ticket type and price (below event name)
    if design_config['ticket_type'] == 'paid':
        price_text = f"PAID ENTRY | ₹{design_config['price']}"
    else:
        price_text = "FREE ENTRY"
    
    draw.text((left_margin, 120), price_text, 
              fill='white', font=subtitle_font)
    
    # Ticket ID (bottom left)
    id_text = f"TICKET ID: {str(ticket_id)[:8].upper()}"
    draw.text((left_margin, height - 80), id_text, 
              fill='white', font=info_font)
    
    # Admit One text
    draw.text((left_margin, height - 50), "ADMIT ONE", 
              fill='white', font=small_font)
    
    # RIGHT SECTION - QR Code in bottom right
    qr = qrcode.QRCode(box_size=6, border=2)
    qr.add_data(str(ticket_id))
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Resize QR code
    qr_size = 130
    qr_img = qr_img.resize((qr_size, qr_size))
    
    # Position QR in bottom right corner
    qr_x = width - qr_size - 30
    qr_y = height - qr_size - 30
    
    # Add white rounded background for QR code
    qr_bg_padding = 15
    qr_bg_rect = [
        qr_x - qr_bg_padding,
        qr_y - qr_bg_padding,
        qr_x + qr_size + qr_bg_padding,
        qr_y + qr_size + qr_bg_padding
    ]
    draw.rounded_rectangle(qr_bg_rect, radius=15, fill='white')
    
    # Paste QR code
    img.paste(qr_img, (qr_x, qr_y))
    
    # Add "SCAN HERE" text above QR
    scan_text = "SCAN HERE"
    bbox = draw.textbbox((0, 0), scan_text, font=small_font)
    text_width = bbox[2] - bbox[0]
    draw.text((qr_x + (qr_size - text_width) // 2, qr_y - 25), 
              scan_text, fill='white', font=small_font)
    
    # Add decorative corner elements
    corner_size = 30
    corner_color = (255, 255, 255, 100)
    
    # Top left corner
    draw.rectangle([(0, 0), (corner_size, 5)], fill=corner_color)
    draw.rectangle([(0, 0), (5, corner_size)], fill=corner_color)
    
    # Top right corner
    draw.rectangle([(width - corner_size, 0), (width, 5)], fill=corner_color)
    draw.rectangle([(width - 5, 0), (width, corner_size)], fill=corner_color)
    
    # Bottom left corner
    draw.rectangle([(0, height - 5), (corner_size, height)], fill=corner_color)
    draw.rectangle([(0, height - corner_size), (5, height)], fill=corner_color)
    
    # Convert to base64 for HTML display
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return img_str, img

# --- DESIGN CONFIGURATOR ---
def design_configurator(request):
    """Render the design configuration page."""
    design = request.session.get('ticket_design', {})
    return render(request, 'design_configurator.html', {'design': design})

def save_design(request):
    """Save ticket design configuration to session."""
    if request.method == 'POST':
        design_config = {
            'event_name': request.POST.get('event_name', 'My Event'),
            'ticket_type': request.POST.get('ticket_type', 'entry'),
            'price': int(request.POST.get('price', 0)),
            'primary_color': request.POST.get('primary_color', '#2563eb'),
            'secondary_color': request.POST.get('secondary_color', '#1e40af'),
            'background_style': request.POST.get('background_style', 'gradient'),
        }
        request.session['ticket_design'] = design_config
        return redirect('/generate/')
    return redirect('/design/')

# --- GENERATOR SECTION ---
def generate_tickets(request):
    """
    Generates N tickets with custom design and displays them for printing/distribution.
    Run this BEFORE the event.
    """
    tickets_to_show = []
    design_config = request.session.get('ticket_design', None)
    
    if request.method == "POST":
        count = int(request.POST.get('count', 5))
        ticket_ids = []
        
        for _ in range(count):
            # Create DB entry
            new_ticket = Ticket.objects.create()
            ticket_ids.append(str(new_ticket.ticket_id))
            
            # Generate custom ticket image
            img_str, _ = generate_ticket_image(new_ticket.ticket_id, design_config)
            
            tickets_to_show.append({
                'id': new_ticket.ticket_id, 
                'qr_image': img_str
            })
        
        # Store ticket IDs in session for download
        request.session['last_generated_tickets'] = ticket_ids

    return render(request, 'generate.html', {
        'tickets': tickets_to_show,
        'design': design_config
    })

def download_tickets_zip(request):
    """
    Downloads the last generated tickets as a ZIP file with custom design.
    """
    ticket_ids = request.session.get('last_generated_tickets', [])
    design_config = request.session.get('ticket_design', None)
    
    if not ticket_ids:
        return HttpResponse("No tickets to download. Please generate tickets first.", status=400)
    
    # Create ZIP file in memory
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for ticket_id in ticket_ids:
            # Generate custom ticket image
            _, img = generate_ticket_image(ticket_id, design_config)
            
            # Save to buffer
            img_buffer = BytesIO()
            img.save(img_buffer, format="PNG")
            img_buffer.seek(0)
            
            # Add to ZIP with filename
            zip_file.writestr(f'ticket_{ticket_id[:8]}.png', img_buffer.getvalue())
    
    # Prepare response
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="event_tickets.zip"'
    
    return response

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