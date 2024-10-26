from gradio_client import Client as GradioClient, file
import os
import cv2

IMAGE_URL = "/home/yellowflash/Magizh-tech/Whatsapp-Twilio-TryOn-Bot/static/result.png"

gradio_client = GradioClient("Nymbo/Virtual-Try-On")

def send_to_gradio():
    # Download both images from Twilio
    person_image_path = "/home/yellowflash/Magizh-tech/Whatsapp-Twilio-TryOn-Bot/WhatsApp Image 2024-10-26 at 7.07.49 PM.jpeg"
    garment_image_path = "/home/yellowflash/Magizh-tech/Whatsapp-Twilio-TryOn-Bot/akatsuki.jpg"

    if person_image_path is None or garment_image_path is None:
        print("Error: One of the images could not be downloaded.")
        return None

    try:
        # Interact with the Gradio API using the client
        result = gradio_client.predict(
            dict={"background": file(person_image_path), "layers": [], "composite": None},
            garm_img=file(garment_image_path),
            garment_des="A cool description of the garment",
            is_checked=True,
            is_checked_crop=False,
            denoise_steps=30,
            seed=42,
            api_name="/tryon",
            
        )

        # Log the result for debugging
        print(f"API result: {result}")

        # Check if the result is returned correctly
        if result and len(result) > 0:
            try_on_image_path = result[0]  # First item in result is the output image path
            print(f"Generated try-on image path: {try_on_image_path}")

            # Ensure the static directory exists
            static_dir = 'static'
            if not os.path.exists(static_dir):
                os.makedirs(static_dir)
                print(f"Created directory: {static_dir}")

            # Make sure the path exists
            if os.path.exists(try_on_image_path):
                # Convert the image to PNG format and save it
                img = cv2.imread(try_on_image_path)
                target_path_png = os.path.join(static_dir, 'result.png')
                cv2.imwrite(target_path_png, img)
                print(f"Image saved to: {target_path_png}")

                # Return the public URL for the image as PNG
                return IMAGE_URL
            else:
                print(f"Image not found at: {try_on_image_path}")
                return None

        print("No image returned from the API.")
        return None

    except Exception as e:
        print(f"Error interacting with Gradio API: {e}")
        return None

send_to_gradio()