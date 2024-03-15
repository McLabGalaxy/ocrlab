
## install OS tools
# sudo apt-get install potrace imagemagick

# pngPath = "samples/invoice1.png"
# bmpPath = "samples/invoice1.bmp"
# svgPath = "samples/invoice1.svg"

# # step-1
# #// Convert PNG to BMP
# convert samples/invoice1.png samples/invoice1.bmp 

# # step-2 
# #// Convert BMP to SVG using Potrace
# potrace -s samples/invoice1.bmp -o samples/invoice1.svg

#// Check if the output file exists

convert samples/shop_receipt_sample1.png samples/shop_receipt_sample1.bmp 
potrace -s samples/shop_receipt_sample1.bmp -o samples/shop_receipt_sample1.svg

# POST https://v2.convertapi.com/convert/jpg/to/svg?Secret=your-api-secret
# Content-Type: application/json
 
# {
#     "Parameters": [
#         {
#             "Name": "File",
#             "FileValue": {
#                 "Name": "my_file.jpg",
#                 "Data": "<Base64 encoded file content>"
#             }
#         },
#         {
#             "Name": "StoreFile",
#             "Value": true
#         }
#     ]
# }