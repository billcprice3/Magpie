from PIL import Image, ImageOps, ImageDraw, ImageFilter
import os
import random
import yaml

def read_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def generate_gradient_canvas(canvas_width, canvas_height, circle_colors):
    # Create a blank canvas for the gradient
    gradient_canvas = Image.new('RGBA', (canvas_width, canvas_height), (255, 255, 255,255))
    draw = ImageDraw.Draw(gradient_canvas)
    
    # Generate and randomize list for random color placement

    cycle_permutation = random.randint(0,1)

    if cycle_permutation == 0:
        cycle = [0, 1, 2, 3]

    elif cycle_permutation == 1:
        cycle = [1, 2, 3, 0]

    elif cycle_permutation == 2:
        cycle = [2, 3, 0, 1]

    elif cycle_permutation == 3:
        cycle = [3, 0, 1, 2]

    
    #Draw rectangles in the four quadrants
    draw.rectangle([0,0,canvas_width/2,canvas_height/2],fill=circle_colors[cycle[0]])
    draw.rectangle([canvas_width/2,0,canvas_width,canvas_height/2],fill=circle_colors[cycle[1]])
    draw.rectangle([canvas_width/2,canvas_height/2,canvas_width,canvas_height],fill=circle_colors[cycle[2]])
    draw.rectangle([0,canvas_height/2,canvas_width/2,canvas_height],fill=circle_colors[cycle[3]])

    # Apply a blur to smooth the gradient transitions
    gradient_canvas = gradient_canvas.filter(ImageFilter.GaussianBlur(radius=canvas_width // 4))
    return gradient_canvas

def generate_random_background(canvas_width=2000, canvas_height=2000):
    # Canvas parameters
    background_color = (255, 255, 255, 255)  # White (RGBA format)

    # Circle parameters
    shape_alpha = int(0.25 * 255)  # 30% opacity
    shape_amount = 50
    max_shape_radius = 800
    min_shape_radius = 100

    palette = random.randint(0,1)    # For the random selection of the color palette. 

    
    if palette == 0:
        # Purplish from BGGenerator
        circle_colors = [
            (0, 255, 255, 255), # cyan
            (0, 0, 255, 255), # blue
            (255, 0, 255, 255), # magenta
            (255, 255, 255, 255),  # white
        ]

    elif palette == 1:
        # Reddish from BGGenerator
        circle_colors = [
            (255, 0, 255, 255),  # pink
            (255, 255, 255, 255),  # white
            (255, 255, 0, 255), # yellow
            (255, 0, 0, 255), # red
        ]

    # Generate the gradient canvas based on the selected palette
    gradient_canvas = generate_gradient_canvas(canvas_width, canvas_height, circle_colors)

    # Create a new blank image for canvas
    canvas = Image.new('RGBA', (canvas_width, canvas_height), background_color)

    # Draw randomly placed partially transparent circles using colors sampled from the gradient canvas
    for _ in range(shape_amount):
        x = random.randint(0, canvas_width - 1)
        y = random.randint(0, canvas_height - 1)
        radius = random.randint(min_shape_radius, max_shape_radius)
    
        # Sample the color from the gradient canvas
        base_color = gradient_canvas.getpixel((x, y))
        color = base_color[:3] + (shape_alpha,)  # Append the alpha value for transparency

        # Create a temporary image for drawing the current circle (same size as the canvas)
        temp_circle_img = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))
        temp_draw = ImageDraw.Draw(temp_circle_img)
    
        # Draw the circle on the temporary image
        temp_draw.ellipse([(x - radius, y - radius), (x + radius, y + radius)], fill=color)
    
        # Composite the temporary image onto the main canvas, blending the current circle
        canvas = Image.alpha_composite(canvas, temp_circle_img)

    # No need to convert canvas to 'RGBA' mode again since it's already in 'RGBA'
    return canvas

def main():  
    # Input and output folder paths
    input_folder = 'Inputs/'
    output_folder = 'Outputs/'

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Default configuration values
    default_config = {
        'delete_input_after_processing': True
    }

    # Make config a global variable
    global config

    # Read in the configuration from the config file
    config_file = 'config.yaml'
    config = read_config(config_file)

    # Update default configuration with actual values from the config file
    config = {**default_config, **config}

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
                
                # Construct the full path of the input file
                file_path = os.path.join(input_folder, filename)
                
                if config['delete_input_after_processing'] == True:
                    # The file has been processed, so we're ready to delete it
                    os.remove(file_path)
                    print(f"Deleted {file_path}")


        except Exception as e:
            print(f"Error processing {filename}: {e}")

    print("*All images have been saved to the output folder.*")

# Global variable declaration; will be initialized in main()
config = None

if __name__ == "__main__":
    main()