# GLOBAL THEME APPLICATION GUIDE

## ✅ YOUR GLOBAL THEME FILES ARE READY

**Location:**
- 📄 `tickets/static/css/enhanced-theme.css` (212 lines)
- 📄 `tickets/static/js/animated-background.js` (120 lines)

---

## 🎨 WHAT THE THEME PROVIDES

### Visual Features
- Dark navy background (#111827)
- Soft purple animated glow background (#8b5cf6)
- Smooth floating gradient purple/blue blobs
- Card hover lift effects
- Purple gradient buttons
- Input focus glow effects
- Consistent 12px rounded corners
- Smooth 0.3s transitions

### Animation Features
- 5 floating purple glow blobs (canvas-based)
- Subtle movement, not flashy
- Behind all content (z-index: -1)
- Performance optimized (60fps)
- Fade-in on page load

---

## 📋 HOW TO APPLY TO EACH PAGE

**For EACH template file, add ONLY these 2 lines:**

### Step 1: Add in `<head>` section

Find the `<head>` tag and add these two lines right after it:

```html
<head>
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/enhanced-theme.css' %}">
    <!-- rest of your head content -->
```

**⚠️ IMPORTANT**: 
- Add `{% load static %}` ONLY if it's not already at the top of the file
- Do NOT remove any existing content
- Do NOT modify any Django tags

---

### Step 2: Add before `</body>` tag

Find the closing `</body>` tag and add this line RIGHT BEFORE it:

```html
    <!-- existing body content -->
    
<script src="{% static 'js/animated-background.js' %}"></script>
</body>
```

---

## 📝 TEMPLATES TO UPDATE

Apply the above 2-step process to these 7 files:

1. ✅ `tickets/templates/index.html`
2. ✅ `tickets/templates/dashboard.html`
3. ✅ `tickets/templates/login.html`
4. ✅ `tickets/templates/register.html`
5. ✅ `tickets/templates/design_configurator.html`
6. ✅ `tickets/templates/generate.html`
7. ✅ `tickets/templates/scanner.html`

---

## 🚫 WHAT NOT TO DO

❌ Do NOT remove Django template tags  
❌ Do NOT modify `{% if %}`, `{% for %}`, `{{ }}` blocks  
❌ Do NOT change form structures  
❌ Do NOT remove existing `<style>` blocks  
❌ Do NOT modify existing JavaScript  
❌ Do NOT regenerate entire HTML files  

---

## ✅ WHAT THE THEME DOES

The CSS file uses `!important` declarations to override existing styles:

- **Body**: Dark navy background, white text
- **Cards**: Purple borders, hover lift effect
- **Buttons**: Purple gradient, glow on hover
- **Inputs**: Dark background, purple focus glow
- **Navbar**: Glassmorphism with blur
- **Headings**: Gradient text effect
- **Scrollbar**: Custom purple styling
- **Alerts**: Color-coded with transparency

The JS file creates a canvas element with animated purple blobs that moves slowly in the background.

---

## 🔧 CUSTOMIZATION OPTIONS

### Change Animation Speed
In `animated-background.js` line 31-32, adjust the multiplier:
```javascript
this.vx = (Math.random() - 0.5) * 0.5;  // Lower = slower
this.vy = (Math.random() - 0.5) * 0.5;  // Higher = faster
```

### Change Background Opacity
In `animated-background.js` line 16:
```javascript
canvas.style.opacity = '0.6';  // 0.0 to 1.0
```

### Change Number of Blobs
In `animated-background.js` line 24:
```javascript
const blobCount = 5;  // Try 3-8 for different effects
```

### Change Purple Accent Color
In `enhanced-theme.css` line 8:
```css
--accent: #8b5cf6;  /* Change to any color */
```

---

## 🧪 TESTING

After adding the 2 lines to each template:

1. Save all files
2. Visit http://localhost:8000/
3. You should see:
   - Purple animated blobs floating in background
   - Dark navy backgrounds
   - Purple glowing buttons
   - Cards lifting on hover
   - Smooth transitions

---

## 🔄 TO REMOVE THEME

Simply delete the 2 lines you added from each template:
- Remove the `<link>` tag from `<head>`
- Remove the `<script>` tag before `</body>`

That's it! The theme is completely non-invasive.

---

## 📊 FILE SIZE REFERENCE

- **CSS**: 4.9 KB (212 lines, minifiable)
- **JS**: 3.5 KB (120 lines, minifiable)
- **Total**: ~8.4 KB (very lightweight)

---

## 💡 EXAMPLE: index.html

**BEFORE:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Event Entry System</title>
    <style>
        /* existing styles */
    </style>
</head>
<body>
    <!-- Django content -->
    {% if request.session.user_id %}
        <!-- content -->
    {% endif %}
</body>
</html>
```

**AFTER:**
```html
<!DOCTYPE html>
<html lang="en">
{% load static %}
<head>
    <meta charset="UTF-8">
    <title>Event Entry System</title>
    <link rel="stylesheet" href="{% static 'css/enhanced-theme.css' %}">
    <style>
        /* existing styles */
    </style>
</head>
<body>
    <!-- Django content -->
    {% if request.session.user_id %}
        <!-- content -->
    {% endif %}

<script src="{% static 'js/animated-background.js' %}"></script>
</body>
</html>
```

**That's it!** Only 2 additional lines, no Django tags modified.
