import subprocess

def capture_image(image_path, width=1024, height=768):
    try:
        # raspistillコマンドを実行して画像をキャプチャ
        subprocess.run(['raspistill', '-o', image_path], check=True)
        print(f"Image captured and saved to {image_path}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to capture image: {e}")

if __name__ == "__main__":
    image_path = '/home/bpm1000/My_Projects/AI_VisitorNotifier/camera/test.jpg'
    capture_image(image_path)
