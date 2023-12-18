#LEGACY CODE

# from PIL import ImageFont, ImageDraw, Image  
# import os

# class Gen:
#     def generator(self, name, classs, status):
    
#         output = 'output/'
    
#         if status=='WINNER':
#             win_path = os.path.join('te mplate', 'winner.png')
        
#         elif status=='RUNNER UP':
#             win_path = os.path.join('template', 'runner.png')

#         elif status=='2ND RUNNER UP':
#             win_path = os.path.join('template', 'runner2.png')

#         else:
#             win_path = os.path.join('template', 'part.png')
        
        
        
#         image = Image.open(win_path)  

#         draw = ImageDraw.Draw(image) 
#         font = ImageFont.truetype("arial.ttf", 32)  

#         draw.text((550, 375), name, font=font, fill=(0, 0, 0))  
#         draw.text((95, 418), classs, font=font, fill=(0, 0, 0))  
        
#         image.save(output + f'{name}{classs}.png') 


