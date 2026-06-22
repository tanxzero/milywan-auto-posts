Milywan Education Auto-Posting Starter v2

Files:
- posts.json: 30 pre-written carousel posts
- create_images.py: turns one post into 5 carousel images
- requirements.txt: Python dependency list
- sample_output_day_01/: generated example carousel images

How to run locally:
1. Install Python 3.10+
2. In this folder, run:
   pip install -r requirements.txt
3. Generate day 1:
   python create_images.py --post-id day_01 --output output
4. Generate another day:
   python create_images.py --post-id day_02 --output output

The images are 1080 x 1350 px, Instagram 4:5 format.
Do not store Meta/Cloudinary/OpenAI secrets directly in code.
