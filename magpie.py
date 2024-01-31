from PIL import Image, ImageOps, ImageDraw
import os
import random

def generate_random_background(canvas_width=2000, canvas_height=2000):
    # Canvas parameters
    background_color = (255, 255, 255, 255)  # White (RGBA format)

    # Circle parameters
    shape_alpha = int(0.3 * 255)  # x% opacity
    shape_amount = 100
    max_shape_radius = 400
    min_shape_radius = 200

    palette = random.randint(0,5)    # For the random selection of the color palette. 
    
    if palette == 0:
        # Analogous: soft blues and greens
        circle_colors = [
            (105, 240, 197, 255),
            (105, 195, 240, 255),
            (105, 238, 240, 255),
            (105, 240, 151, 255),
            (105, 153, 240, 255),
        ]
        
    elif palette == 1:
        # Analogous: soft purples and blues
        circle_colors = [
            (115, 101, 240, 255),
            (206, 101, 240, 255),
            (162, 101, 240, 255),
            (101, 130, 240, 255),
            (240, 101, 217, 255),
        ]

    elif palette == 2:
        # Analogous: bold reds and oranges
        circle_colors = [
            (240, 60, 17, 255),
            (240, 138, 17, 255),
            (240, 97, 16, 255),
            (240, 20, 17, 255),
            (240, 167, 17, 255),
        ]
        
    elif palette == 3:
        # Analogous: soft pinky purply
        circle_colors = [
            (239, 173, 240, 255),
            (240, 176, 173, 255),
            (240, 172, 200, 255),
            (217, 173, 240, 255),
            (240, 188, 173, 255),
        ]
        
    elif palette == 4:
        # Original red
        circle_colors = [
            (252, 162, 57, 255),   # Neon Carrot
            (252, 38, 116, 255),   # Radical Red
            (252, 138, 245, 255),   # Lavender Rose
            (252, 241, 119, 255),   # Marigold Yellow
            (252, 140, 168, 255),   # Tickle Me Pink
            (252, 140, 99, 255),   # Salmon
            (252, 228, 225, 255),   # Cindarella
            (252, 20, 44, 255),   # Torch Red
            (252, 60, 188, 255),   # Razzle Dazzle Rose 
        ]
        
    elif palette == 5:
        # Original blue-purple
        circle_colors = [
            (201, 84, 252, 255),   # Heliotrope
            (30, 203, 252, 255),   # Bright Turquoise
            (42, 20, 252, 255),    # Blue
            (157, 169, 252, 255),  # Melrose
            (228, 213, 252, 255),  # Perfume
            (80, 98, 252, 255),    # Dodger Blue
            (176, 32, 252, 255),   # Electric Violet
            (97, 187, 252, 255),   # Malibu
            (72, 154, 252, 255),   # Dodger Blue 2
        ]
        

    # Create a new blank image
    canvas = Image.new('RGBA', (canvas_width, canvas_height), background_color)
    draw = ImageDraw.Draw(canvas)

    # Draw randomly placed partially transparent circles with different blend modes
    blend_modes = ['add', 'multiply', 'screen', 'overlay']

    for _ in range(shape_amount):
        x = random.randint(0, canvas_width)
        y = random.randint(0, canvas_height)
        radius = random.randint(min_shape_radius, max_shape_radius)
        color = random.choice(circle_colors)
        blend_mode = random.choice(blend_modes)

        # Create a circle with the specified fill color and opacity
        circle = Image.new('RGBA', (2 * radius, 2 * radius), (0, 0, 0, 0))
        circle_draw = ImageDraw.Draw(circle)
        circle_draw.ellipse([(0, 0), (2 * radius, 2 * radius)], fill=color)

        # Create a new blank RGBA image of the same size as the canvas
        circle_layer = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))

        # Paste the circle onto the circle_layer using the chosen blend mode
        circle_layer.paste(circle, (x - radius, y - radius))
        circle_layer = Image.alpha_composite(canvas.convert('RGBA'), circle_layer)

        circle_layer.putalpha(shape_alpha)

        # Composite the circle onto the canvas
        canvas = Image.alpha_composite(canvas, circle_layer)

    return canvas

# Input and output folder paths
input_folder = 'Inputs/'
output_folder = 'Outputs/'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Iterate through all image files in the input folder
for filename in os.listdir(input_folder):
    try:
        # Open the image
        with Image.open(os.path.join(input_folder, filename)) as img:

            if img.height / img.width > 1.15:
                canvas = generate_random_background(2000, 2500)
                # Calculate the scaling factor to fit within a 2000x2500 rectangle
                max_width = 1800
                max_height = 2300
                width, height = img.size
                scale_factor = min(max_width / width, max_height / height)

                # Resize img proportionally
                new_width = int(width * scale_factor)
                new_height = int(height * scale_factor)
                img = img.resize((new_width, new_height), Image.LANCZOS)
            else:
                canvas = generate_random_background()
                # Calculate the scaling factor to fit within a 1800x1800 square
                max_dimension = 1800
                width, height = img.size
                scale_factor = min(max_dimension / width, max_dimension / height)

                # Resize img proportionally
                new_width = int(width * scale_factor)
                new_height = int(height * scale_factor)
                img = img.resize((new_width, new_height), Image.LANCZOS)

            # Calculate the position to center the image on the canvas
            x_offset = (canvas.width - new_width - 30) // 2
            y_offset = (canvas.height - new_height - 30) // 2

            # Add a 10px white border to all sides
            img_with_border = ImageOps.expand(img, border=15, fill='white')

            canvas.paste(img_with_border, (x_offset, y_offset))

            # Save the modified image to the output folder
            output_filename = os.path.join(output_folder, os.path.splitext(filename)[0] + '.png')

            canvas.save(output_filename, 'PNG')

            print(f"{filename} has been processed.")
    except Exception as e:
        print(f"Error processing {filename}: {e}")

print("*Images with white borders and a random reddish or purplish background have been saved to the output folder.*")
